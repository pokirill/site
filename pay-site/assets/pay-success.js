/* Возврат с оплаты: опрос статуса подписки.

   Успешный редирект банка НЕ означает, что деньги пришли - подтверждение
   приходит на api.kubysh.com отдельным уведомлением с задержкой. Поэтому
   здесь опрос, а не сообщение «оплачено» по факту возврата.

   Вынесено из разметки под строгий CSP: политика запрещает инлайновые
   скрипты, потому что именно через инлайн уводят сессию, если на страницу
   попадает чужой код. */
(function () {
  'use strict';
  var Api = window.PayApi, Session = window.PaySession, U = window.PayUtils;
  var PLAN_TITLES = { year: 'Год', month: 'Месяц' };

  function $(id) { return document.getElementById(id); }
  function show(id) {
    ['state-checking', 'state-done', 'state-pending', 'state-signin'].forEach(function (s) {
      var el = $(s), hide = s !== id;
      el.classList.toggle('hidden', hide);
      el.hidden = hide;   // работает и без CSS
    });
    window.scrollTo(0, 0);
  }

  var params = new URLSearchParams(window.location.search);
  var order = params.get('order') || '';
  if (order) {
    // Номер заказа показываем только в состоянии ожидания: он нужен поддержке,
    // а в успешном сценарии это лишний шум.
    $('order-hint').textContent = 'Номер платежа для поддержки: ' + order;
  }

  function renderDone(sub) {
    $('done-plan').textContent = PLAN_TITLES[sub.plan] || sub.plan || '—';
    $('done-until').textContent = U.formatDate(sub.valid_until) || '—';
    show('state-done');
  }

  function check() {
    show('state-checking');
    U.pollSubscription(function (elapsed, total) {
      $('checking-progress').textContent = elapsed + ' из ' + total + ' с';
    }).then(function (result) {
      if (result.ok) renderDone(result.subscription);
      else show('state-pending');
    });
  }

  $('retry-btn').addEventListener('click', check);

  if (!Session.isSignedIn()) show('state-signin');
  else check();
})();
