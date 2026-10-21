/* Remove the short-lived ticket before loading any external script. */
(function () {
  'use strict';
  var params = new URLSearchParams(window.location.hash.slice(1));
  window.PayHandoffTicket = params.get('checkout_handoff');
  if (window.PayHandoffTicket) {
    history.replaceState(null, '', window.location.pathname + window.location.search);
  }
})();
