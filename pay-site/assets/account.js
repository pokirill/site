/* Логика личного кабинета: четыре состояния из постановки плюс два служебных.

   не вошёл -> (провайдер не дал почту) -> подписки нет -> подписка есть
                                                              -> продление отключено

   Состояния переключаются показом/скрытием секций, а не перерисовкой: так
   проще отлаживать в браузере и не теряется фокус на полях ввода. */

(function () {
  'use strict';

  var CFG = window.PAY_CONFIG || {};
  var Api = window.PayApi;
  var Session = window.PaySession;
  var U = window.PayUtils;
  var Auth = window.PayAuth;

  var PLAN_TITLES = { year: 'Год', month: 'Месяц' };

  var state = {
    plans: [],
    currency: 'RUB',
    selectedPlan: null,
    subscription: null,
  };

  function $(id) { return document.getElementById(id); }

  // CHECKOUT-STEPS-1: какой экран кабинета увидел человек.
  var STEP_BY_STATE = { 'state-signin': 'signin_shown', 'state-contact': 'contact_shown', 'state-plans': 'plans_shown' };

  function show(id) {
    if (STEP_BY_STATE[id]) Api.step(STEP_BY_STATE[id]);
    var sections = ['state-loading', 'state-signin', 'state-contact',
                    'state-plans', 'state-active', 'state-confirm-cancel'];
    sections.forEach(function (s) {
      var el = $(s);
      if (!el) return;
      var hide = s !== id;
      el.classList.toggle('hidden', hide);
      // Атрибут hidden дублирует класс: если CSS не доехал, состояния всё
      // равно не покажутся все сразу - браузер понимает hidden без стилей.
      el.hidden = hide;
    });
    // Наверх при смене экрана: иначе после отмены человек видит середину страницы
    window.scrollTo(0, 0);
  }

  function showError(id, message) {
    notice(id, message, 'error');
  }

  /* Плашка сообщения. `kind` решает вид: 'error' - что-то сломалось и это надо
     починить, 'info' - так и задумано (функция выключена, продление отключено).
     Одинаковый красный на оба случая заставляет человека искать свою ошибку
     там, где её нет. */
  function notice(id, message, kind) {
    var el = $(id);
    if (!el) return;
    el.textContent = message;
    el.classList.toggle('notice--error', kind !== 'info');
    el.classList.toggle('notice--info', kind === 'info');
    el.classList.remove('hidden');
    el.hidden = false;
  }

  function hideError(id) {
    var el = $(id);
    if (!el) return;
    el.classList.add('hidden');
    // Атрибут снимаем тоже: `notice` его ставит, и без этой строки плашка,
    // однажды показанная, больше не скрылась бы - класс скрывает, атрибут нет.
    el.hidden = true;
  }

  function busy(button, isBusy, labelWhenBusy) {
    if (!button) return;
    if (isBusy) {
      button.dataset.label = button.textContent;
      button.textContent = labelWhenBusy || 'Секунду…';
      button.disabled = true;
    } else {
      if (button.dataset.label) button.textContent = button.dataset.label;
      button.disabled = false;
    }
  }

  /* ---------- Вход ----------

     Единственный способ - Apple (см. pay-auth.js). Окно входа открывает сам
     Apple, адрес appleid.apple.com человек видит и может проверить; ни пароль,
     ни код двухфакторки на нашей странице не появляются. */

  var signInBound = false;

  function bindSignIn() {
    if (signInBound) return;
    signInBound = true;
    var button = $('apple-signin');
    if (!button) return;
    button.addEventListener('click', function () {
      hideError('signin-error');
      busy(button, true, 'Открываем Apple…');
      Auth.signIn().then(function (data) {
        // null означает, что человек сам закрыл окно Apple - это не ошибка
        if (!data) { busy(button, false); return; }
        Session.save(data);
        afterSignIn();
      }).catch(function (error) {
        busy(button, false);
        showError('signin-error', error.message || 'Не получилось войти. Попробуй ещё раз.');
      });
    });

    if (!Auth.isConfigured()) {
      showError('signin-error', 'Вход пока не настроен. Напиши нам, включим вручную.');
    }
  }

  function afterSignIn() {
    var account = Session.account();
    // Без контакта оплату начинать нельзя: чек по 54-ФЗ надо доставить
    if (account && account.needs_contact) {
      show('state-contact');
      return;
    }
    loadSubscription();
  }

  /* ---------- Контакт для чека ---------- */

  function bindContact() {
    var form = $('contact-form');
    if (!form) return;
    form.addEventListener('submit', function (event) {
      event.preventDefault();
      hideError('contact-error');

      var email = ($('contact-email').value || '').trim();
      var phone = ($('contact-phone').value || '').trim();

      if (!email && !phone) {
        showError('contact-error', 'Оставь почту или телефон — на них придёт чек.');
        return;
      }
      if (email && email.indexOf('@') === -1) {
        showError('contact-error', 'Проверь адрес почты.');
        return;
      }

      var button = $('contact-submit');
      busy(button, true, 'Сохраняем…');
      Api.saveContact(email, phone).then(function () {
        Session.setContactDone();
        loadSubscription();
      }).catch(function (error) {
        busy(button, false);
        showError('contact-error', error.message);
      });
    });
  }

  /* ---------- Откуда пришел человек ---------- */

  // PAY-CONTEXT-1: placement приходит с сервера при открытии чекаута из приложения.
  // sessionStorage, а не localStorage: заход на сайт напрямую позже не должен
  // получить заголовок про закрытый период.
  var CONTEXT_KEY = 'kubysh_checkout_placement';
  var CONTEXTS = {
    close_period: {
      title: 'Период закрыт. Продолжим план?',
      lead: 'Ты уже видел Кубыш в деле: план до получки, бюджет на день, итоги периода. ' +
            'Подписка открывает следующий период, а серия, цели и вся история остаются на месте.'
    },
    // support появится с PAY-PLACEMENT-SUPPORT-1 (iOS 1.7.6), до этого кнопка поддержки шлет cabinet.
    support: {
      title: 'Спасибо, что решил поддержать Кубыш',
      lead: 'Ты уже знаешь, как он помогает: спокойный план до получки, бюджет на день и цели с понятными сроками. ' +
            'Подписка сохраняет все это и дает Кубышу работать дальше.'
    },
    cabinet: {
      title: 'Кубыш живет на подписках',
      lead: 'Ты уже знаешь, как он помогает: спокойный план до получки, бюджет на день и цели с понятными сроками. ' +
            'Подписка сохраняет все это и дает Кубышу работать дальше.'
    }
  };

  function savePlacement(placement) {
    try { sessionStorage.setItem(CONTEXT_KEY, placement || ''); } catch (e) { /* приватный режим */ }
  }

  function applyContext() {
    var placement = null;
    try { placement = sessionStorage.getItem(CONTEXT_KEY); } catch (e) { placement = null; }
    var context = CONTEXTS[placement];
    if (!context) return;
    var personal = placement === 'close_period' ? personalContext(readFact()) : null;
    $('plans-title').textContent = (personal || context).title;
    $('plans-lead').textContent = (personal || context).lead;
  }

  /* ---------- PAYWALL-PERSONAL-1: довод из приложения ---------- */

  // Те же цифры, что человек только что видел на пейволе. Суммы считает приложение,
  // сайт их только показывает. Обещание: «Комфортно сегодня, спокойно завтра».
  function readFact() {
    var raw = null;
    try { raw = sessionStorage.getItem('kubysh_checkout_fact'); } catch (e) { raw = null; }
    if (!raw) return null;
    var parts = raw.split(':');
    var amount = parseInt(parts[1], 10);
    if (!(amount > 0)) return null;
    return { kind: parts[0], amount: amount, days: parseInt(parts[2], 10) || 0 };
  }

  function readDepositRub() {
    var raw = null;
    try { raw = sessionStorage.getItem('kubysh_checkout_deposit'); } catch (e) { raw = null; }
    var rub = parseInt(raw, 10);
    return rub > 0 ? rub : null;
  }

  function rub(amount) { return U.formatMoney(amount * 100, 'RUB'); }

  function daysWord(n) {
    var m10 = n % 10, m100 = n % 100;
    if (m10 === 1 && m100 !== 11) return 'день';
    if (m10 >= 2 && m10 <= 4 && (m100 < 12 || m100 > 14)) return 'дня';
    return 'дней';
  }

  function personalContext(fact) {
    if (!fact) return null;
    var tail = 'Подписка открывает следующий период: сумма на день, подушка и цели по плану. ' +
               'Серия, цели и вся история остаются на месте.';
    if (fact.kind === 'shortfall_avoided') {
      return {
        title: 'Ты дошёл до получки без минуса',
        lead: 'За ' + fact.days + ' ' + daysWord(fact.days) + ' до получки Кубыш увидел, что может не хватить ' +
              rub(fact.amount) + ', и ты успел выровнять траты. ' + tail
      };
    }
    if (fact.kind === 'saved') {
      return { title: 'За период ты сэкономил ' + rub(fact.amount), lead: 'Эти деньги остались у тебя. ' + tail };
    }
    if (fact.kind === 'accumulated') {
      return { title: 'С Кубышем ты накопил ' + rub(fact.amount), lead: tail };
    }
    return null;
  }

  // Вклад против цены подписки в месяц: показываем, только если вклад приносит больше.
  function updateDepositLine(plan) {
    var line = $('plans-deposit');
    if (!line) return;
    var deposit = readDepositRub();
    var perMonthKopecks = plan ? (plan.code === 'year' ? plan.per_month : plan.price) : null;
    if (!deposit || !perMonthKopecks || deposit * 100 <= perMonthKopecks) {
      line.hidden = true;
      return;
    }
    line.textContent = 'Вклад, который Кубыш подобрал под твои накопления, по сегодняшним ставкам приносит около ' +
      rub(deposit) + ' в месяц. Подписка стоит ' + U.formatMoneyRounded(perMonthKopecks, state.currency) + ' в месяц.';
    line.hidden = false;
  }

  /* ---------- Тарифы ---------- */

  function renderPlans() {
    var list = $('plans-list');
    if (!list) return;
    list.innerHTML = '';

    // Год первым и крупнее - решено в постановке
    var order = { year: 0, month: 1 };
    var sorted = state.plans.slice().sort(function (a, b) {
      return (order[a.code] === undefined ? 9 : order[a.code]) -
             (order[b.code] === undefined ? 9 : order[b.code]);
    });

    var month = sorted.filter(function (p) { return p.code === 'month'; })[0];

    sorted.forEach(function (plan) {
      var button = document.createElement('button');
      button.type = 'button';
      button.className = 'plan' + (plan.code === 'year' ? ' plan--year' : '');
      button.setAttribute('aria-pressed', 'false');
      button.dataset.plan = plan.code;

      var isYear = plan.code === 'year';
      var note = isYear
        ? 'Все цели в работе, и год можно не думать о деньгах'
        : 'Если ещё присматриваешься';

      button.innerHTML =
        '<span class="plan-head">' +
          '<span class="plan-title"></span>' +
          '<span class="plan-price"></span>' +
        '</span>' +
        (isYear ? '<span class="plan-total"></span>' : '') +
        '<span class="plan-note"></span>';

      // Через textContent, а не в шаблон: название приходит с сервера
      button.querySelector('.plan-title').textContent = plan.title || PLAN_TITLES[plan.code] || plan.code;
      button.querySelector('.plan-note').textContent = note;

      if (isYear) {
        // PRICE-2: в годе главная цифра - цена месяца, списание за год рядом и мельче.
        // Сумма списания всё равно названа явно: здесь и в блоке «Перед оплатой».
        var price = button.querySelector('.plan-price');
        price.textContent = U.formatMoneyRounded(plan.per_month, state.currency);
        var unit = document.createElement('span');
        unit.className = 'plan-unit';
        unit.textContent = '/мес';
        price.appendChild(unit);

        var total = U.formatMoney(plan.price, state.currency) + ' за год';
        // «По цене 7 месяцев» понятнее процента скидки и не переносится на телефоне.
        var months = month ? Math.ceil(plan.price / month.price) : 12;
        if (months < 12) total += ' · по цене ' + months + ' месяцев';
        button.querySelector('.plan-total').textContent = total;
      } else {
        button.querySelector('.plan-price').textContent = U.formatMoney(plan.price, state.currency);
      }

      button.addEventListener('click', function () {
        selectPlan(plan.code);
        Api.step('plan_selected', plan.code); // только нажатие человека, не тариф по умолчанию
      });
      list.appendChild(button);
    });

    // Год предвыбран: он основной. Это не срочность и не давление, просто
    // разумный дефолт - переключить можно одним нажатием.
    var hasYear = sorted.some(function (p) { return p.code === 'year'; });
    selectPlan(hasYear ? 'year' : (sorted[0] && sorted[0].code));
  }

  function selectPlan(code) {
    if (!code) return;
    state.selectedPlan = code;
    var buttons = document.querySelectorAll('.plan');
    Array.prototype.forEach.call(buttons, function (button) {
      button.setAttribute('aria-pressed', String(button.dataset.plan === code));
    });

    var plan = state.plans.filter(function (p) { return p.code === code; })[0];
    var period = $('terms-period');
    if (plan && period) {
      var every = code === 'year' ? 'раз в год' : 'раз в месяц';
      period.textContent = 'Списание ' + U.formatMoney(plan.price, state.currency) +
        ' ' + every + ' с карты, которой оплатил.';
    }
    var button = $('pay-btn');
    if (plan && button && !button.disabled) {
      button.textContent = 'Оплатить ' + U.formatMoney(plan.price, state.currency);
    }
    // Цена в день против пакетика растворимого кофе (15-30 ₽ в магазине): сравнение
    // верно для обоих тарифов, пока день дешевле 15 ₽.
    updateDepositLine(plan);
    var anchor = $('plans-anchor');
    if (plan && anchor) {
      var perDay = Math.round(plan.price / 100 / (code === 'year' ? 365 : 30));
      anchor.hidden = perDay >= 15;
      anchor.textContent = 'Это ' + perDay + ' ₽ в день. Дешевле пакетика растворимого кофе, ' +
        'а помогает дожить до получки спокойно и дойти до целей.';
    }
    updatePayButton();
  }

  function updatePayButton() {
    var button = $('pay-btn');
    var consent = $('consent');
    var hint = $('pay-hint');
    if (!button || !consent) return;

    // Кнопка активна всегда: «мертвая» серая кнопка выглядит как сбой. Без
    // согласия нажатие подсвечивает галочку (см. bindPay). Ставить галочку за
    // человека нельзя: согласие на регулярные списания должно быть явным.
    if (consent.checked) $('consent-row').classList.remove('consent--attention');
    if (hint) {
      hint.textContent = consent.checked || !hint.dataset.nudged
        ? 'Дальше откроется страница оплаты Т-Банка.'
        : 'Отметь согласие с условиями, и откроем оплату.';
    }
  }

  function bindPay() {
    var consent = $('consent');
    if (consent) consent.addEventListener('change', function () {
      if (consent.checked) Api.step('consent_checked', state.selectedPlan);
      updatePayButton();
    });

    var button = $('pay-btn');
    if (!button) return;
    button.addEventListener('click', function () {
      if (!state.selectedPlan) return;
      Api.step('pay_tapped', state.selectedPlan); // нажатие, даже если галочки ещё нет
      if (!consent || !consent.checked) {
        var row = $('consent-row');
        row.classList.remove('consent--attention');
        void row.offsetWidth; // перезапуск анимации при повторном нажатии
        row.classList.add('consent--attention');
        $('pay-hint').dataset.nudged = '1';
        updatePayButton();
        return;
      }
      hideError('plans-error');
      busy(button, true, 'Готовим оплату…');

      Api.startPayment(state.selectedPlan).then(function (data) {
        if (!data || !data.payment_url) {
          throw new U.ApiError('Не удалось открыть оплату. Попробуй ещё раз.', 0);
        }
        // Уходим на форму банка. Карту рисует он, мы её не видим.
        window.location.href = data.payment_url;
      }).catch(function (error) {
        busy(button, false);
        // Оплата ещё не подключена (503) - это состояние, а не сбой. Красная
        // плашка здесь врёт: человек ничего не сделал неправильно, и повторять
        // попытку бессмысленно. Показываем спокойно и даём контакт поддержки.
        if (error && error.status === 503) {
          notice('plans-error', error.message, 'info');
          return;
        }
        showError('plans-error', error.message);
      });
    });
  }

  /* ---------- Активная подписка ---------- */

  function renderActive(sub) {
    var title = PLAN_TITLES[sub.plan] || sub.plan || '—';
    $('active-plan').textContent = title;
    $('active-until').textContent = U.formatDate(sub.valid_until) || '—';

    var renew = $('active-renew');
    renew.innerHTML = '';
    var badge = document.createElement('span');
    badge.className = 'badge ' + (sub.will_renew ? 'badge--on' : 'badge--off');
    badge.textContent = sub.will_renew ? 'Включено' : 'Отключено';
    renew.appendChild(badge);

    var renewBlock = $('renew-block');
    var done = $('cancel-done');

    if (sub.will_renew) {
      renewBlock.classList.remove('hidden');
      done.classList.add('hidden');
    } else {
      // Состояние «продление отключено»: пишем прямым текстом, до какого
      // числа сохранится доступ. Это требование постановки.
      renewBlock.classList.add('hidden');
      done.textContent = 'Продление отключено. Доступ останется до ' +
        (U.formatDate(sub.valid_until) || 'конца оплаченного срока') + '.';
      done.classList.remove('hidden');
    }
  }

  function bindCancel() {
    var openButton = $('cancel-btn');
    if (openButton) {
      openButton.addEventListener('click', function () {
        var sub = state.subscription;
        var explain = $('cancel-explain');
        if (explain && sub) {
          explain.textContent = 'Доступ останется до ' +
            (U.formatDate(sub.valid_until) || 'конца оплаченного срока') +
            '. После этого Кубыш перейдёт в бесплатный режим — данные никуда не пропадут.';
        }
        show('state-confirm-cancel');
      });
    }

    var back = $('cancel-back');
    if (back) back.addEventListener('click', function () { show('state-active'); });

    var confirm = $('cancel-confirm');
    if (confirm) {
      confirm.addEventListener('click', function () {
        busy(confirm, true, 'Отключаем…');
        Api.cancel().then(function () {
          busy(confirm, false);
          return loadSubscription();
        }).catch(function (error) {
          busy(confirm, false);
          show('state-active');
          showError('active-error', error.message);
        });
      });
    }
  }

  function bindSignOut() {
    var button = $('signout-btn');
    if (!button) return;
    button.addEventListener('click', function () {
      Session.clear();
      Auth.signOut();
      show('state-signin');
    });
  }

  /* ---------- Загрузка ---------- */

  function loadSubscription() {
    show('state-loading');
    return Api.subscription().then(function (sub) {
      state.subscription = sub;
      if (sub && sub.has_subscription) {
        renderActive(sub);
        show('state-active');
        return;
      }
      return loadPlans();
    }).catch(function (error) {
      if (error.status === 401 || error.status === 403) {
        show('state-signin');
        showError('signin-error', 'Сессия истекла. Войди заново.');
        return;
      }
      // Подписку не прочитали, но человек вошёл: показываем тарифы и ошибку,
      // а не пустой экран. Хуже пустого экрана только пустой экран без объяснения.
      return loadPlans().then(function () {
        showError('plans-error', error.message);
      });
    });
  }

  function loadPlans() {
    return Api.plans().then(function (data) {
      state.plans = (data && data.plans) || [];
      state.currency = (data && data.currency) || 'RUB';
      if (!state.plans.length) {
        show('state-plans');
        showError('plans-error', 'Тарифы сейчас недоступны. Попробуй обновить страницу.');
        return;
      }
      applyContext();
      renderPlans();
      show('state-plans');
    }).catch(function (error) {
      show('state-plans');
      showError('plans-error', error.message);
    });
  }

  function init() {
    bindSignIn();
    bindContact();
    bindPay();
    bindCancel();
    bindSignOut();

    // Разбора возврата из адресной строки здесь больше нет: токен приходит в
    // колбэк Apple (режим popup) и в URL не попадает вообще. Это убирает целый
    // канал утечки - историю браузера, логи прокси и Referer.
    var ticket = window.PayHandoffTicket;
    window.PayHandoffTicket = null;
    if (ticket) {
      history.replaceState(null, '', window.location.pathname + window.location.search);
      show('state-loading');
      Api.openCheckout(ticket).then(function (data) {
        savePlacement(data && data.placement);
        if (Session.isSignedIn()) afterSignIn();
        else show('state-signin');
      }).catch(function () {
        Session.clear();
        show('state-signin');
        showError('signin-error', 'Ссылка истекла. Открой личный кабинет ещё раз из приложения.');
      });
    } else if (Session.isSignedIn()) {
      afterSignIn();
    } else {
      show('state-signin');
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
