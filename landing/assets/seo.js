(function(){
  var id=44147844;
  window.ym=window.ym||function(){(window.ym.a=window.ym.a||[]).push(arguments)};
  window.ym.l=1*new Date();
  var s=document.createElement('script'),x=document.getElementsByTagName('script')[0];
  s.async=true;s.src='https://mc.yandex.ru/metrika/tag.js';x.parentNode.insertBefore(s,x);
  window.ym(id,'init',{clickmap:true,trackLinks:true,accurateTrackBounce:true});
  document.addEventListener('click',function(e){
    var a=e.target.closest && e.target.closest('a.js-appstore');
    if(a) window.ym(id,'reachGoal','seo_appstore_click',{page:location.pathname});
  });
  function n(id){var el=document.getElementById(id);return el?Number(String(el.value).replace(/[^0-9.,-]/g,'').replace(',','.'))||0:0}
  function money(v){return Math.max(0,Math.ceil(v)).toLocaleString('ru-RU')+' ₽'}
  function savings(){var o=document.getElementById('savings-output');if(!o)return;var target=n('target'),start=n('start'),months=Math.max(1,n('months'));o.value='Откладывать примерно '+money((target-start)/months)+' в месяц';o.textContent=o.value}
  function cushion(){var o=document.getElementById('cushion-output');if(!o)return;var spend=n('essential'),months=Math.max(1,n('cushion-months'));o.value='Ориентир: '+money(spend*months);o.textContent=o.value}
  ['target','start','months'].forEach(function(id){var e=document.getElementById(id);if(e)e.addEventListener('input',savings)});
  ['essential','cushion-months'].forEach(function(id){var e=document.getElementById(id);if(e)e.addEventListener('input',cushion)});
  savings();cushion();
})();
