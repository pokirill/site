/* Вход через Apple. Единственный способ входа — решение от 01.09.2026.

   Бэкенд умеет Apple: на неверный токен отвечает 401 Invalid Apple token,
   то есть проверяет подпись, audience, issuer, срок жизни и nonce.

   ## Почему popup, а не редирект

   Apple умеет два режима. При редиректе браузер уходит на appleid.apple.com и
   возвращается POST-запросом на наш адрес — тогда токен приходит в теле формы, а
   страница перезагружается. При popup токен приходит в JS-промис, а адресная
   строка вообще не меняется. Второй вариант безопаснее: токена нет ни в истории
   браузера, ни в логах прокси, ни в Referer, и человек не может случайно
   отправить кому-то ссылку вместе с ним.

   ## Почему SDK грузится до клика

   Popup должен открываться в рамках пользовательского жеста. Если начать
   загружать SDK только ПОСЛЕ клика и открыть popup после сетевого await, Safari
   и SFSafariViewController могут уже потерять user activation и заблокировать
   окно. Симптом выглядит ровно как «вход через раз»: первая попытка только
   успевает загрузить SDK, вторая работает. Поэтому account/index.html грузит
   Apple SDK заранее, а этот файл использует его синхронно. Динамическая
   загрузка остаётся только запасным путём на случай старого кеша страницы.

   ## Nonce: защита от повторного использования токена

   Перед входом генерируем случайное значение и передаём его Apple. Apple
   вкладывает его внутрь подписанного токена. Мы отправляем на бэкенд и токен, и
   это значение — бэкенд сверяет их и запоминает, что nonce использован.

   Значение генерируем через crypto.getRandomValues, а не Math.random:
   Math.random предсказуем и для защиты не годится.

   ## Что мы НЕ делаем

   Токен Apple нигде не сохраняем: он уходит на наш бэкенд и забывается.
   В localStorage лежит только наша сессия.

   Имя и почту, которые Apple отдаёт РЯДОМ с токеном (поле user), на бэкенд не
   пересылаем. Это обычные строки от клиента, их может подменить кто угодно.
   Почта берётся бэкендом из подписанного токена, и только оттуда.

   ## Про почту Apple

   Apple отдаёт почту ТОЛЬКО при первой авторизации, и часто это скрытый адрес
   вида ...@privaterelay.appleid.com. Отказываться от такого адреса нельзя: чеки
   по нему доходят. Но если почты в токене нет вовсе, оплату начинать нельзя —
   по 54-ФЗ чек надо доставить, поэтому кабинет спросит контакт (needs_contact). */

(function () {
  'use strict';

  var CFG = window.PAY_CONFIG || {};
  var SDK = 'https://appleid.cdn-apple.com/appleauth/static/jsapi/appleid/1/ru_RU/appleid.auth.js';
  var sdkPromise = null;

  function sdkReady() {
    return !!(window.AppleID && window.AppleID.auth);
  }

  function loadSdk() {
    if (sdkReady()) return Promise.resolve();
    if (sdkPromise) return sdkPromise;
    sdkPromise = new Promise(function (resolve, reject) {
      var el = document.createElement('script');
      el.src = SDK;
      el.async = true;
      el.defer = true;
      el.onload = function () {
        if (sdkReady()) resolve();
        else reject(new Error('Apple загрузился без модуля входа. Обнови страницу.'));
      };
      el.onerror = function () {
        sdkPromise = null;
        reject(new Error('Не удалось загрузить вход Apple. Проверь связь и попробуй ещё раз.'));
      };
      document.head.appendChild(el);
    });
    return sdkPromise;
  }

  /* Случайная строка для nonce и state. Криптостойкий источник обязателен:
     предсказуемое значение защиты не даёт. */
  function randomToken() {
    var bytes = new Uint8Array(32);
    if (window.crypto && window.crypto.getRandomValues) {
      window.crypto.getRandomValues(bytes);
    } else {
      throw new Error('Браузер слишком старый для безопасного входа. Обнови его.');
    }
    var out = '';
    for (var i = 0; i < bytes.length; i++) {
      out += ('0' + bytes[i].toString(16)).slice(-2);
    }
    return out;
  }

  var pending = null;   // { nonce, state } текущей попытки входа

  function beginAppleSignIn(nonce, state) {
    if (!sdkReady()) {
      return Promise.reject(new Error('Вход Apple ещё загружается. Обнови страницу и попробуй снова.'));
    }
    try {
      window.AppleID.auth.init({
        // Service ID из Apple Developer, а НЕ Bundle ID приложения.
        clientId: CFG.appleServiceId,
        scope: 'name email',
        redirectURI: CFG.appleRedirectUri,
        state: state,
        nonce: nonce,
        // Токен приходит в промис, адресная строка не меняется.
        usePopup: true,
      });
      return window.AppleID.auth.signIn();
    } catch (error) {
      return Promise.reject(error);
    }
  }

  function signIn() {
    if (!CFG.appleServiceId) {
      return Promise.reject(new Error('Вход пока не настроен. Напиши нам, включим вручную.'));
    }

    var nonce, state;
    try {
      nonce = randomToken();
      state = randomToken();
    } catch (e) {
      return Promise.reject(e);
    }
    pending = { nonce: nonce, state: state };

    // Нормальный путь: SDK уже загружен самой страницей, поэтому signIn()
    // вызывается прямо в обработчике клика и popup не теряет user activation.
    // Запасной путь нужен только старому закешированному HTML без preload.
    var signInPromise = sdkReady()
      ? beginAppleSignIn(nonce, state)
      : loadSdk().then(function () { return beginAppleSignIn(nonce, state); });

    return signInPromise.then(function (result) {
      var token = result && result.authorization && result.authorization.id_token;
      if (!token) throw new Error('Apple не вернул данные для входа. Попробуй ещё раз.');

      // state сверяем на своей стороне: ответ должен относиться к нашей попытке.
      var returned = result.authorization.state;
      if (returned && pending && returned !== pending.state) {
        throw new Error('Не удалось подтвердить вход. Попробуй ещё раз.');
      }

      var payload = { identity_token: token };
      if (pending && pending.nonce) payload.nonce = pending.nonce;
      pending = null;

      // Имя и почту из result.user намеренно НЕ отправляем: это данные от
      // клиента, их можно подменить. Бэкенд берёт почту из подписанного токена.
      return window.PayApi.auth('apple', payload);
    }).catch(function (error) {
      pending = null;
      // Человек сам закрыл окно Apple — это не ошибка, показывать нечего.
      var code = error && (error.error || (error.details && error.details.error));
      if (code === 'popup_closed_by_user' || code === 'user_cancelled_authorize' ||
          code === 'user_trigger_new_signin_flow') {
        return null;
      }
      if (code === 'invalid_client') {
        throw new Error('Вход настроен неверно: Apple не признаёт наш Service ID. Мы уже разбираемся.');
      }
      throw error;
    });
  }

  window.PayAuth = {
    signIn: signIn,
    prepare: loadSdk,
    isConfigured: function () { return !!CFG.appleServiceId; },
    // У Apple нет клиентского состояния, которое надо сбрасывать при выходе:
    // сессию мы держим сами. Метод оставлен, чтобы кабинету было что вызвать.
    signOut: function () { pending = null; },
  };

  // Прогреваем SDK сразу. На актуальном account/index.html он уже загружен и
  // вызов мгновенный; на старом кеше это сокращает шанс, что первый клик
  // придётся на сетевую загрузку SDK.
  loadSdk().catch(function () { /* ошибку покажет signIn при реальной попытке */ });
})();
