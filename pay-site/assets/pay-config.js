/* Настройки страниц оплаты. ЕДИНСТВЕННЫЙ файл, который надо править при
   подключении входа: ключи вписываются здесь, в разметку не лезем.

   ## Что получить

   1. `appleServiceId` — **Service ID**, а НЕ Bundle ID приложения.
      Apple Developer → Certificates, Identifiers & Profiles → Identifiers →
      фильтр **Services IDs** → создать, включить Sign in with Apple.

      🚨 В настройках этого Service ID обязательно указать:
      - Primary App ID: **тот же App ID, что у приложения Кубыш**.
        От этого зависит связка сайта и приложения: Apple выдаёт один и тот же
        идентификатор пользователя (`sub`) только внутри одной группы. Выберете
        другой Primary App ID — и один человек получит ДВА разных аккаунта:
        подписка, купленная на сайте, в приложении не появится.
      - Domains: `pay.kubysh.com`
      - Return URLs: `https://pay.kubysh.com/account/`
        Совпадать должно символ в символ, включая слэш. Расхождение — и Apple
        ответит `invalid_client`.

   2. Приватный ключ для Sign in with Apple (файл `.p8`), Key ID и Team ID —
      нужны БЭКЕНДУ, не сюда. На странице секретов нет и быть не может: этот
      файл отдаётся всем. Если ключ когда-нибудь окажется здесь, его надо
      считать скомпрометированным и отзывать.

   ## Что проверяет бэкенд

   Он уже умеет Apple: на неверный токен отвечает 401 Invalid Apple token.
   Важно, чтобы в список допустимых `aud` попали ОБА значения — Service ID для
   сайта и Bundle ID для приложения. Токены у них разные, а аккаунт один. */

window.PAY_CONFIG = {
  // Бэкенд живёт на отдельном домене - запросы кросс-доменные.
  // CORS на стороне API настроен на kubysh.com, www.kubysh.com и pay.kubysh.com.
  apiBase: 'https://api.kubysh.com/v1',

  // Service ID из Apple Developer (НЕ Bundle ID приложения `app.kubyshka`).
  // Проверено 02.09.2026 обращением к самому Apple: с этим client_id и нашим
  // redirect_uri `https://pay.kubysh.com/account/` отдаётся страница входа, а не
  // `invalid_client` — значит Service ID существует, домен и Return URL в нём
  // зарегистрированы. Совпадает со значением по умолчанию `apple_service_id`
  // на бэкенде, поэтому оба `aud` уже допустимы.
  appleServiceId: 'com.kubysh.web',

  // Адрес возврата. Даже в режиме popup Apple требует, чтобы он был
  // зарегистрирован и совпадал символ в символ.
  appleRedirectUri: 'https://pay.kubysh.com/account/',

  // Опрос статуса после возврата с оплаты: успешный редирект не означает, что
  // деньги пришли - подтверждение приходит на бэкенд отдельным уведомлением.
  pollIntervalMs: 2000,
  pollTimeoutMs: 30000,

  supportUrl: 'https://t.me/kubyshka_user',
};
