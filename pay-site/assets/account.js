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

  function show(id) {
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

    sorted.forEach(function (plan) {
      var button = document.createElement('button');
      button.type = 'button';
      button.className = 'plan' + (plan.code === 'year' ? ' plan--year' : '');
      button.setAttribute('aria-pressed', 'false');
      button.dataset.plan = plan.code;

      var note = plan.code === 'year'
        ? U.formatMoneyRounded(plan.per_month, state.currency) +
          ' в месяц. Все цели в работе, и год можно не думать о деньгах'
        : 'Если ещё присматриваешься';

      button.innerHTML =
        '<span class="plan-head">' +
          '<span class="plan-title"></span>' +
          '<span class="plan-price"></span>' +
        '</span>' +
        '<span class="plan-note"></span>';

      // Через textContent, а не в шаблон: название приходит с сервера
      button.querySelector('.plan-title').textContent = plan.title || PLAN_TITLES[plan.code] || plan.code;
      button.querySelector('.plan-price').textContent = U.formatMoney(plan.price, state.currency);
      button.querySelector('.plan-note').textContent = note;

      button.addEventListener('click', function () { selectPlan(plan.code); });
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
    updatePayButton();
  }

  function updatePayButton() {
    var button = $('pay-btn');
    var consent = $('consent');
    var hint = $('pay-hint');
    if (!button || !consent) return;

    var ready = !!state.selectedPlan && consent.checked;
    button.disabled = !ready;

    if (hint) {
      if (!state.selectedPlan) hint.textContent = 'Выбери тариф и отметь согласие с условиями.';
      else if (!consent.checked) hint.textContent = 'Отметь согласие с условиями, чтобы продолжить.';
      else hint.textContent = 'Дальше откроется страница оплаты Т-Банка.';
    }
  }

  function bindPay() {
    var consent = $('consent');
    if (consent) consent.addEventListener('change', updatePayButton);

    var button = $('pay-btn');
    if (!button) return;
    button.addEventListener('click', function () {
      if (!state.selectedPlan) return;
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
    if (Session.isSignedIn()) {
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
