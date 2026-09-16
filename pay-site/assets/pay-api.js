/* Слой работы с API и сессией. Один файл на все страницы оплаты.

   Почему сессия в localStorage, а не в cookie: API живёт на другом домене
   (api.kubysh.com), сторонние cookie в Safari блокируются по умолчанию, а
   страница обязана работать внутри SFSafariViewController в приложении.
   Токен кладётся в заголовок Authorization вручную - это работает всегда. */

(function () {
  'use strict';

  var CFG = window.PAY_CONFIG || {};
  var TOKEN_KEY = 'kubysh_session_token';
  var ACCOUNT_KEY = 'kubysh_account';

  /* --- Хранилище. В приватном режиме localStorage может кидать исключение,
     поэтому каждое обращение обёрнуто: страница должна работать и без него,
     просто сессия не переживёт перезагрузку. --- */
  var memory = {};

  function store(key, value) {
    memory[key] = value;
    try {
      if (value === null) localStorage.removeItem(key);
      else localStorage.setItem(key, value);
    } catch (e) { /* приватный режим или запрет на хранение */ }
  }

  function read(key) {
    if (Object.prototype.hasOwnProperty.call(memory, key)) return memory[key];
    try { return localStorage.getItem(key); } catch (e) { return null; }
  }

  var Session = {
    token: function () { return read(TOKEN_KEY); },
    isSignedIn: function () { return !!read(TOKEN_KEY); },
    save: function (data) {
      store(TOKEN_KEY, data.session_token);
      store(ACCOUNT_KEY, JSON.stringify({
        account_id: data.account_id,
        email: data.email || '',
        needs_contact: !!data.needs_contact,
      }));
    },
    account: function () {
      var raw = read(ACCOUNT_KEY);
      if (!raw) return null;
      try { return JSON.parse(raw); } catch (e) { return null; }
    },
    setContactDone: function () {
      var acc = Session.account() || {};
      acc.needs_contact = false;
      store(ACCOUNT_KEY, JSON.stringify(acc));
    },
    clear: function () {
      store(TOKEN_KEY, null);
      store(ACCOUNT_KEY, null);
      delete memory[TOKEN_KEY];
      delete memory[ACCOUNT_KEY];
    },
  };

  /* --- Ошибки с человеческим текстом. Ключевое: сообщение показывается
     пользователю, поэтому в нём не должно быть кодов и англицизмов. --- */
  function ApiError(message, status) {
    this.name = 'ApiError';
    this.message = message;
    this.status = status || 0;
  }
  ApiError.prototype = Object.create(Error.prototype);

  function humanMessage(status, detail) {
    if (status === 401 || status === 403) return 'Сессия истекла. Войди заново.';
    if (status === 402) return 'Оплата не прошла. Попробуй другую карту.';
    if (status === 404) return 'Не нашли данные. Обнови страницу.';
    if (status === 429) return 'Слишком много запросов. Подожди минуту.';
    // 503 - это НЕ поломка: так бэкенд говорит «функция пока выключена»
    // (например, реквизиты банка ещё не заведены). Своим текстом мы бы
    // отправили человека «пробовать через минуту» и он бы жал кнопку по кругу.
    if (status === 503 && detail) return detail;
    if (status >= 500) return 'Сервис ненадолго недоступен. Попробуй через минуту.';
    if (detail) return detail;
    return 'Что-то пошло не так. Попробуй ещё раз.';
  }

  function request(path, options) {
    options = options || {};
    var headers = { 'Accept': 'application/json' };
    if (options.body) headers['Content-Type'] = 'application/json';
    var token = Session.token();
    if (token && options.auth !== false) headers['Authorization'] = 'Bearer ' + token;

    // Свой таймаут: без него зависший запрос оставляет кнопку в спиннере навсегда
    var controller = typeof AbortController !== 'undefined' ? new AbortController() : null;
    var timer = controller ? setTimeout(function () { controller.abort(); }, options.timeoutMs || 20000) : null;

    return fetch(CFG.apiBase + path, {
      method: options.method || 'GET',
      headers: headers,
      body: options.body ? JSON.stringify(options.body) : undefined,
      signal: controller ? controller.signal : undefined,
      credentials: 'omit',
    }).then(function (response) {
      if (timer) clearTimeout(timer);
      return response.text().then(function (text) {
        var data = null;
        if (text) { try { data = JSON.parse(text); } catch (e) { data = null; } }
        if (!response.ok) {
          // Истёкшую сессию гасим сразу, иначе страница будет биться в 401
          if (response.status === 401 || response.status === 403) Session.clear();
          throw new ApiError(
            humanMessage(response.status, data && data.detail),
            response.status
          );
        }
        return data;
      });
    }).catch(function (error) {
      if (timer) clearTimeout(timer);
      if (error instanceof ApiError) throw error;
      if (error && error.name === 'AbortError') {
        throw new ApiError('Сервис долго не отвечает. Проверь связь и попробуй ещё раз.', 0);
      }
      throw new ApiError('Нет связи с сервисом. Проверь интернет.', 0);
    });
  }

  var Api = {
    auth: function (provider, payload) {
      return request('/web/auth/' + provider, {
        method: 'POST', body: payload, auth: false,
      });
    },
    saveContact: function (email, phone) {
      return request('/web/contact', {
        method: 'POST',
        body: { email: email || null, phone: phone || null },
      });
    },
    plans: function () { return request('/web/plans', { auth: false }); },
    subscription: function () { return request('/web/subscription'); },
    startPayment: function (plan) {
      return request('/web/payments/start', { method: 'POST', body: { plan: plan } });
    },
    cancel: function () {
      return request('/web/subscription/cancel', { method: 'POST' });
    },
  };

  /* --- Деньги. Приходят В КОПЕЙКАХ, и дробным числом их нигде держать нельзя:
     округление копейки на паре тысяч операций даёт расхождение с банком. --- */
  /* Округление до рубля - только для справочных подписей вида «416 ₽ в месяц».
     Для сумм списания использовать formatMoney: там копейки обязательны. */
  function formatMoneyRounded(kopecks, currency) {
    return formatMoney(Math.round(kopecks / 100) * 100, currency);
  }

  function formatMoney(kopecks, currency) {
    var whole = Math.floor(Math.abs(kopecks) / 100);
    var cents = Math.abs(kopecks) % 100;
    var sign = kopecks < 0 ? '-' : '';
    var spaced = String(whole).replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
    var symbols = { RUB: ' ₽', KZT: ' ₸', BYN: ' BYN', USD: ' $' };
    var suffix = symbols[currency] || (currency ? ' ' + currency : '');
    return sign + spaced + (cents ? ',' + String(cents).padStart(2, '0') : '') + suffix;
  }

  var MONTHS = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
                'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'];

  function formatDate(iso) {
    if (!iso) return '';
    var d = new Date(iso);
    if (isNaN(d.getTime())) return '';
    return d.getDate() + ' ' + MONTHS[d.getMonth()] + ' ' + d.getFullYear();
  }

  /* --- Опрос статуса подписки после возврата с оплаты.
     Нужен потому, что редирект банка НЕ означает поступление денег:
     подтверждение приходит на бэкенд отдельным уведомлением с задержкой. --- */
  function pollSubscription(onTick) {
    var started = Date.now();
    var interval = CFG.pollIntervalMs || 2000;
    var limit = CFG.pollTimeoutMs || 30000;

    return new Promise(function (resolve) {
      function attempt() {
        Api.subscription().then(function (sub) {
          if (sub && sub.has_subscription) return resolve({ ok: true, subscription: sub });
          next();
        }).catch(function () {
          // Ошибку в опросе глотаем: подписка могла ещё не появиться, а
          // показывать человеку ошибку в момент ожидания платежа - худшее,
          // что можно сделать.
          next();
        });
      }
      function next() {
        var elapsed = Date.now() - started;
        if (elapsed >= limit) return resolve({ ok: false, timedOut: true });
        if (onTick) onTick(Math.round(elapsed / 1000), Math.round(limit / 1000));
        setTimeout(attempt, interval);
      }
      attempt();
    });
  }

  window.PayApi = Api;
  window.PaySession = Session;
  window.PayUtils = {
    formatMoney: formatMoney,
    formatMoneyRounded: formatMoneyRounded,
    formatDate: formatDate,
    pollSubscription: pollSubscription,
    ApiError: ApiError,
  };
})();
