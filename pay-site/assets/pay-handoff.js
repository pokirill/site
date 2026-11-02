/* Remove the short-lived ticket before loading any external script. */
(function () {
  'use strict';
  var params = new URLSearchParams(window.location.hash.slice(1));
  // HANDOFF-QUERY-1 (02.11): Safari при холодном запуске из приложения терял фрагмент — страница открывалась
  // без билета и показывала вход вместо тарифов (≈40% переходов). Сервер теперь кладёт билет в query;
  // фрагмент читаем для старых ссылок. Билет одноразовый и живёт 30 минут, из адреса убирается сразу.
  var query = new URLSearchParams(window.location.search);
  window.PayHandoffTicket = params.get('checkout_handoff') || query.get('checkout_handoff');
  if (query.has('checkout_handoff')) {
    query.delete('checkout_handoff');
    var rest = query.toString();
    history.replaceState(null, '', window.location.pathname + (rest ? '?' + rest : '') + window.location.hash);
  }
  if (window.PayHandoffTicket) {
    // PAYWALL-PERSONAL-1: довод пейвола из приложения (только суммы). Во фрагменте он не уходит на
    // сервер; проверяет и показывает его account.js, здесь только переносим в sessionStorage.
    try {
      var fact = params.get('fact');
      var deposit = params.get('deposit');
      if (fact && /^(shortfall_avoided:\d{1,9}:\d{1,3}|saved:\d{1,9}|accumulated:\d{1,9})$/.test(fact)) {
        sessionStorage.setItem('kubysh_checkout_fact', fact);
      } else {
        sessionStorage.removeItem('kubysh_checkout_fact');
      }
      if (deposit && /^\d{1,9}$/.test(deposit)) sessionStorage.setItem('kubysh_checkout_deposit', deposit);
      else sessionStorage.removeItem('kubysh_checkout_deposit');
      // PAY-PLACEMENT-FLAGS-1 (iOS 1.7.6): флаги источника — только счётчики и итог недели, без идентификаторов.
      // days — дней с Кубышем, tx — трат в периоде, week — неделя в плане (under) или сверх (over) на N ₽.
      var FLAGS = { days: /^\d{1,4}$/, tx: /^\d{1,5}$/, week: /^(under|over):\d{1,9}$/ };
      Object.keys(FLAGS).forEach(function (key) {
        var value = params.get(key);
        if (value && FLAGS[key].test(value)) sessionStorage.setItem('kubysh_checkout_' + key, value);
        else sessionStorage.removeItem('kubysh_checkout_' + key);
      });
    } catch (e) { /* приватный режим: просто без личной строки */ }
    history.replaceState(null, '', window.location.pathname + window.location.search);
  }
})();
