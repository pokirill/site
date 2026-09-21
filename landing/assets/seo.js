(function(){
  var METRIKA_ID=112718911;
  var CONSENT_KEY='kubysh_cookie_consent_v2';
  var metrikaStarted=false;

  function consent(){
    try{return localStorage.getItem(CONSENT_KEY)}catch(e){return null}
  }
  function setConsent(value){
    try{localStorage.setItem(CONSENT_KEY,value)}catch(e){}
  }
  function startMetrika(){
    if(metrikaStarted||!METRIKA_ID)return;
    metrikaStarted=true;
    window.ym=window.ym||function(){(window.ym.a=window.ym.a||[]).push(arguments)};
    window.ym.l=1*new Date();
    var s=document.createElement('script'),x=document.getElementsByTagName('script')[0];
    s.async=true;
    s.src='https://mc.yandex.ru/metrika/tag.js';
    x.parentNode.insertBefore(s,x);
    window.ym(METRIKA_ID,'init',{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:true});
  }
  function goal(name,params){
    if(metrikaStarted&&window.ym)window.ym(METRIKA_ID,'reachGoal',name,params);
  }
  function showConsent(){
    if(consent()||document.getElementById('cookieBar'))return;
    var bar=document.createElement('div');
    bar.className='cookie-bar';
    bar.id='cookieBar';
    bar.setAttribute('role','region');
    bar.setAttribute('aria-label','Согласие на использование cookie');
    bar.innerHTML='<p class="cookie-bar__text">Мы используем файлы cookie, в том числе для статистики посещений. Подробнее — в <a href="/privacy/">политике конфиденциальности</a>.</p><div class="cookie-bar__btns"><button type="button" class="cookie-bar__no" data-consent="no">Только необходимое</button><button type="button" class="cookie-bar__yes" data-consent="yes">Принять</button></div>';
    document.body.appendChild(bar);
    window.setTimeout(function(){bar.classList.add('cookie-bar--in')},30);
    bar.addEventListener('click',function(e){
      var button=e.target.closest&&e.target.closest('[data-consent]');
      if(!button)return;
      var value=button.getAttribute('data-consent');
      setConsent(value);
      if(value==='yes')startMetrika();
      bar.parentNode.removeChild(bar);
    });
  }

  if(location.search.indexOf('cookie=reset')>-1){
    try{localStorage.removeItem(CONSENT_KEY)}catch(e){}
  }
  if(consent()==='yes')startMetrika();

  document.addEventListener('DOMContentLoaded',function(){
    showConsent();
    savings();
    cushion();
  });

  document.addEventListener('click',function(e){
    var link=e.target.closest&&e.target.closest('a.js-appstore');
    if(!link)return;
    var params={page:location.pathname};
    goal('appstore_click',params);
    goal('seo_appstore_click',params);
  },true);

  function n(id){var el=document.getElementById(id);return el?Number(String(el.value).replace(/[^0-9.,-]/g,'').replace(',','.'))||0:0}
  function money(v){return Math.max(0,Math.ceil(v)).toLocaleString('ru-RU')+' ₽'}
  function savings(){var o=document.getElementById('savings-output');if(!o)return;var target=n('target'),start=n('start'),months=Math.max(1,n('months'));o.value='Откладывать примерно '+money((target-start)/months)+' в месяц';o.textContent=o.value}
  function cushion(){var o=document.getElementById('cushion-output');if(!o)return;var spend=n('essential'),months=Math.max(1,n('cushion-months'));o.value='Ориентир: '+money(spend*months);o.textContent=o.value}
  ['target','start','months'].forEach(function(id){var e=document.getElementById(id);if(e)e.addEventListener('input',savings)});
  ['essential','cushion-months'].forEach(function(id){var e=document.getElementById(id);if(e)e.addEventListener('input',cushion)});
})();
