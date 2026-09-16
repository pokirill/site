/* Номер платежа из адреса - в подсказку для поддержки.
   Вынесено из разметки, чтобы CSP мог запретить инлайновые скрипты:
   именно через инлайн крадут сессию, если на страницу попадает чужой код. */
(function () {
  var order = new URLSearchParams(window.location.search).get('order');
  if (order) {
    document.getElementById('order-hint').textContent = 'Номер платежа для поддержки: ' + order;
  }
})();
