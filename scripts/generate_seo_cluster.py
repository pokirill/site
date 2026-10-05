#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the kubysh.com organic-acquisition cluster.

The pages are intentionally grouped by search intent, not one page per keyword.
Personal finance is YMYL: every page shows methodology/sources and avoids
personalized investment or credit advice.
"""
from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANDING = ROOT / "landing"
# Спецстраница App Store «Лендинг» (ppid): переходы с сайта видны отдельно в App Store Connect
APP_STORE = "https://apps.apple.com/us/app/%D0%BA%D1%83%D0%B1%D1%8B%D1%88-%D0%BB%D0%B8%D1%87%D0%BD%D1%8B%D0%B5-%D1%84%D0%B8%D0%BD%D0%B0%D0%BD%D1%81%D1%8B-%D0%B1%D1%8E%D0%B4%D0%B6%D0%B5%D1%82/id6778792103?ppid=ad248954-9df5-4e1e-9f9e-236a70021ad9"
MAIN_MODIFIED_DATE = "2026-10-05"
PUBLISHED_DATE = "2026-09-15"
MODIFIED_DATE = "2026-09-18"
HUB_MODIFIED_DATE = "2026-09-19"
SITE_NAME = "Кубыш"
SITE_URL = "https://kubysh.com/"
SOCIAL_IMAGE = "https://kubysh.com/og-cover.jpg"
ABOUT_IMAGE = "https://kubysh.com/img/kirill-popov.jpg"
SEO_ASSET_VERSION = "20261005b"
SEO_JS_VERSION = "20261005b"

CSS = r"""*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}body{margin:0;background:#000;color:#fff;font:17px/1.64 Inter,system-ui,-apple-system,sans-serif;-webkit-font-smoothing:antialiased}a{color:#cef16c}header{position:sticky;top:0;z-index:10;background:rgba(0,0,0,.88);backdrop-filter:blur(14px);border-bottom:1px solid rgba(255,255,255,.12)}.wrap{width:min(760px,calc(100% - 36px));margin:auto}.top{height:60px;display:flex;align-items:center;justify-content:space-between;gap:16px}.logo{font:700 20px/1 system-ui;text-decoration:none;color:#fff;letter-spacing:-.04em}.logo span{color:#cef16c}.topnav{display:flex;gap:14px;align-items:center}.topnav a{font-size:14px;text-decoration:none}.install{border:1px solid rgba(206,241,108,.4);border-radius:999px;padding:7px 13px}.crumbs{padding-top:30px;color:rgba(255,255,255,.48);font-size:13px}.crumbs a{color:rgba(255,255,255,.6)}main{padding-bottom:28px}h1,h2,h3{font-family:system-ui,-apple-system,sans-serif;letter-spacing:-.035em;line-height:1.12}h1{font-size:clamp(32px,7vw,48px);margin:18px 0 18px}h2{font-size:clamp(23px,4vw,30px);margin:44px 0 14px}h3{font-size:19px;margin:26px 0 8px}p{color:rgba(255,255,255,.8);margin:0 0 15px}.lead{font-size:20px;color:#fff;border-left:2px solid #cef16c;padding-left:17px;margin-bottom:28px}.answer{background:rgba(206,241,108,.08);border:1px solid rgba(206,241,108,.26);border-radius:16px;padding:18px 20px;margin:24px 0}.answer strong{color:#cef16c}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}.card{display:block;background:rgba(255,255,255,.045);border:1px solid rgba(255,255,255,.12);border-radius:15px;padding:17px;text-decoration:none;color:#fff}.card strong{display:block;margin-bottom:4px}.card span{display:block;color:rgba(255,255,255,.57);font-size:14px}.card:hover{border-color:rgba(206,241,108,.45)}ul,ol{padding-left:22px;color:rgba(255,255,255,.8)}li{margin:7px 0}.steps{counter-reset:s}.steps li{padding-left:5px}.note{font-size:14px;color:rgba(255,255,255,.54);border-left:1px solid rgba(255,255,255,.2);padding-left:13px}.tool{background:rgba(255,255,255,.045);border:1px solid rgba(255,255,255,.13);border-radius:18px;padding:20px;margin:24px 0}.tool label{display:block;font-size:14px;color:rgba(255,255,255,.65);margin:10px 0 5px}.tool input{width:100%;font:inherit;color:#fff;background:#151515;border:1px solid rgba(255,255,255,.15);border-radius:12px;padding:12px 13px}.tool output{display:block;margin-top:16px;font-size:22px;font-weight:700;color:#cef16c}.faq details{border-bottom:1px solid rgba(255,255,255,.12);padding:15px 0}.faq summary{cursor:pointer;font-weight:650;list-style:none}.faq summary::-webkit-details-marker{display:none}.faq p{margin-top:10px}.cta{margin:46px 0 20px;padding:24px;background:rgba(255,255,255,.045);border:1px solid rgba(206,241,108,.25);border-radius:18px;text-align:center}.cta h2{margin:0 0 10px}.btn{display:inline-block;margin-top:8px;background:#cef16c;color:#090909;text-decoration:none;border-radius:999px;padding:13px 24px;font-weight:700}.related{margin-top:38px}.sources{font-size:14px;color:rgba(255,255,255,.55)}.sources li{margin:5px 0}.updated{font-size:13px;color:rgba(255,255,255,.42);margin-top:26px}footer{border-top:1px solid rgba(255,255,255,.12);margin-top:50px;padding:26px 0 38px;color:rgba(255,255,255,.5);font-size:13px}footer .links{display:flex;flex-wrap:wrap;gap:8px 17px;margin-bottom:10px}footer a{color:rgba(255,255,255,.68)}.cookie-bar{position:fixed;left:16px;right:16px;bottom:16px;z-index:1000;display:flex;align-items:center;gap:18px;max-width:920px;margin:auto;padding:14px 16px;background:rgba(18,18,18,.96);border:1px solid rgba(255,255,255,.2);border-radius:16px;box-shadow:0 18px 56px rgba(0,0,0,.46);font-size:13px;line-height:1.35;opacity:0;transform:translateY(20px);transition:opacity .2s ease,transform .2s ease}.cookie-bar--in{opacity:1;transform:translateY(0)}.cookie-bar__text{margin:0;flex:1 1 auto;color:rgba(255,255,255,.82)}.cookie-bar__text a{color:#cef16c;text-underline-offset:3px}.cookie-bar__btns{display:flex;gap:8px;flex:0 0 auto}.cookie-bar button{font:inherit;border:1px solid rgba(255,255,255,.35);border-radius:999px;padding:9px 13px;cursor:pointer}.cookie-bar__no{background:transparent;color:#fff}.cookie-bar__yes{background:#cef16c;color:#0d0d0d;border-color:#cef16c!important}.app{display:grid;grid-template-columns:190px minmax(0,1fr);gap:24px;align-items:center;margin:28px 0;padding:22px;border:1px solid rgba(206,241,108,.25);border-radius:20px;background:rgba(255,255,255,.04)}.app img{display:block;width:100%;height:auto}.app h2{margin:0 0 10px}.app ul{margin:0 0 14px}.app .btn{margin-top:0}.app .note{margin:12px 0 0;border:0;padding:0}@media(max-width:620px){.app{grid-template-columns:96px minmax(0,1fr);gap:14px;padding:16px}}.download{margin:28px 0;padding:22px;border-radius:20px;background:#cef16c;color:#0a0a0a}.download h2{margin:0 0 8px;color:#0a0a0a}.download p{color:rgba(0,0,0,.72)}.download .btn{background:#0a0a0a;color:#fff;margin:6px 8px 0 0}.download .note{color:rgba(0,0,0,.6);border-color:rgba(0,0,0,.2);margin-top:12px}.data{width:100%;border-collapse:collapse;margin:16px 0 22px;font-size:15px}.data th,.data td{text-align:left;padding:9px 10px;border-bottom:1px solid rgba(255,255,255,.12)}.data td:last-child,.data th:last-child{text-align:right;white-space:nowrap}.data tr.total td{font-weight:700;color:#cef16c}@media(max-width:620px){.wrap{width:min(100% - 30px,760px)}.grid{grid-template-columns:1fr}.topnav .hub{display:none}h1{font-size:34px}.lead{font-size:18px}.card{padding:15px}.cookie-bar{flex-direction:column;align-items:stretch;gap:10px}.cookie-bar__btns{width:100%}.cookie-bar button{flex:1 1 50%}}@media(prefers-reduced-motion:reduce){.cookie-bar{transition:none}}""".strip()

MATERIALS_CSS = r"""
.materials-intro{margin:34px 0 56px;padding:30px;border:1px solid rgba(206,241,108,.24);border-radius:24px;background:radial-gradient(circle at 90% 10%,rgba(113,55,220,.2),transparent 42%),rgba(255,255,255,.035)}.materials-intro-label{margin:0 0 10px;color:#cef16c;font-size:12px;font-weight:750;letter-spacing:.12em;text-transform:uppercase}.materials-intro p:last-child{max-width:650px;margin:0;color:rgba(255,255,255,.72);font-size:18px}.materials-about{margin:54px 0 12px}.materials-about h2{margin-bottom:18px}.materials-about-intro{max-width:650px;color:rgba(255,255,255,.62)}.materials-about-grid{display:grid;grid-template-columns:1.15fr .85fr;gap:12px;margin-top:22px}.materials-about-card{position:relative;overflow:hidden;display:flex;flex-direction:column;min-height:270px;padding:24px;border:1px solid rgba(255,255,255,.14);border-radius:22px;background:linear-gradient(145deg,rgba(113,55,220,.15),rgba(255,255,255,.025));color:#fff;text-decoration:none;transition:transform .2s,border-color .2s}.materials-about-card:hover{transform:translateY(-2px);border-color:rgba(206,241,108,.48)}.materials-about-card:focus-visible{outline:2px solid #cef16c;outline-offset:4px}.materials-about-card small{position:relative;z-index:2;color:#cef16c;font-size:12px;font-weight:750;letter-spacing:.1em;text-transform:uppercase}.materials-about-card strong{position:relative;z-index:2;display:block;max-width:430px;margin:42px 0 12px;font-size:clamp(24px,3.8vw,34px);line-height:1.03;letter-spacing:-.04em}.materials-about-card span{position:relative;z-index:2;display:block;max-width:380px;color:rgba(255,255,255,.62);font-size:15px;line-height:1.5}.materials-about-card b{position:relative;z-index:2;margin-top:auto;color:#cef16c;font-size:22px;font-weight:400}.materials-about-card--story{background:linear-gradient(100deg,#130f19 0%,#0c0c0d 64%)}.materials-about-card--story strong,.materials-about-card--story span{max-width:57%}.materials-about-photo{position:absolute;right:-4%;bottom:-18%;width:49%;height:115%;object-fit:cover;object-position:center top;opacity:.68;filter:saturate(.82)}.materials-about-card--story:after{content:"";position:absolute;z-index:1;inset:0;background:linear-gradient(90deg,#130f19 34%,rgba(19,15,25,.88) 53%,transparent 82%);pointer-events:none}.materials-about-card--method{background:radial-gradient(circle at 90% 10%,rgba(206,241,108,.11),transparent 38%),linear-gradient(145deg,#111509,#090909 64%)}@media(max-width:620px){.materials-intro{margin:26px 0 44px;padding:22px}.materials-intro p:last-child{font-size:16px}.materials-about{margin-top:44px}.materials-about-grid{grid-template-columns:1fr}.materials-about-card{min-height:260px}.materials-about-card--story{min-height:300px}.materials-about-card--story strong,.materials-about-card--story span{max-width:68%}.materials-about-photo{right:-10%;bottom:-8%;width:55%;height:90%}}
""".strip()

MATERIALS_BLOCK = '''
<section class="materials-about" aria-labelledby="materials-about-title">
  <h2 id="materials-about-title">О Кубыше</h2>
  <p class="materials-about-intro">История продукта и принципы, по которым мы объясняем финансовые расчёты</p>
  <div class="materials-about-grid">
    <a class="materials-about-card materials-about-card--story" href="/o-proekte/">
      <small>История проекта</small>
      <strong>Кирилл, Фича и путь к Кубышу</strong>
      <span>От личного вопроса о деньгах до приложения в App Store</span>
      <b aria-hidden="true">→</b>
      <img class="materials-about-photo" src="/img/kirill-popov.jpg" width="746" height="810" alt="" loading="lazy" decoding="async">
    </a>
    <a class="materials-about-card materials-about-card--method" href="/metodologiya/">
      <small>Как мы считаем</small>
      <strong>Формулы, источники и границы</strong>
      <span>Почему расчётам можно доверять и где заканчивается образовательный материал</span>
      <b aria-hidden="true">→</b>
    </a>
  </div>
</section>
'''.strip()

ABOUT_CSS = r"""
.about-wrap{width:min(1040px,calc(100% - 36px));margin:auto}.about-main{padding-bottom:36px}.about-hero{display:grid;grid-template-columns:minmax(0,1.2fr) minmax(280px,.8fr);gap:clamp(34px,5vw,60px);align-items:center;padding:64px 0 40px}.about-kicker{display:inline-flex;align-items:center;gap:9px;margin:0 0 28px;color:#cef16c;font-size:13px;font-weight:700;letter-spacing:.09em;text-transform:uppercase}.about-kicker:before{content:"";width:8px;height:8px;border-radius:50%;background:#cef16c;box-shadow:0 0 22px rgba(206,241,108,.65)}.about-name{display:flex;align-items:center;gap:14px;margin:0 0 15px;color:rgba(255,255,255,.58);font-size:clamp(18px,2vw,23px);font-weight:650;letter-spacing:-.02em}.about-name:after{content:"";width:44px;height:1px;background:rgba(255,255,255,.24)}.about-hero h1{font-size:clamp(46px,6.1vw,72px);line-height:.98;margin:0 0 28px;max-width:720px;letter-spacing:-.045em}.about-hero h1 span{display:block;color:#cef16c}.about-lead{max-width:660px;color:#fff;font-size:clamp(20px,2.4vw,27px);line-height:1.35;margin:0 0 24px}.about-role{display:inline-flex;flex-wrap:wrap;gap:8px 12px;align-items:center;color:rgba(255,255,255,.6);font-size:14px}.about-role strong{color:#fff}.about-photo-wrap{position:relative}.about-photo-wrap:before{content:"";position:absolute;inset:-10% -12%;background:radial-gradient(circle,rgba(113,55,220,.36),transparent 67%);filter:blur(18px)}.about-photo{position:relative;display:block;width:100%;height:auto;border-radius:32px;border:1px solid rgba(255,255,255,.18);box-shadow:0 30px 90px rgba(0,0,0,.48)}.about-caption{position:relative;margin:11px 4px 0;color:rgba(255,255,255,.45);font-size:13px}.about-section{padding:52px 0;border-top:1px solid rgba(255,255,255,.12)}.about-section h2{font-size:clamp(30px,5vw,50px);max-width:780px;margin:0 0 22px}.about-copy{max-width:780px}.about-copy p{font-size:clamp(18px,2vw,21px);line-height:1.62}.about-quote{margin:32px 0 0;padding:25px 28px;border:1px solid rgba(206,241,108,.28);border-radius:22px;background:linear-gradient(135deg,rgba(206,241,108,.11),rgba(113,55,220,.08));font-size:clamp(22px,3vw,31px);line-height:1.28;letter-spacing:-.025em;color:#fff}.about-principles{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin-top:28px}.about-principle{padding:22px;border:1px solid rgba(255,255,255,.13);border-radius:20px;background:rgba(255,255,255,.045)}.about-principle b{display:block;margin-bottom:8px;font-size:18px}.about-principle p{font-size:15px;line-height:1.5;margin:0;color:rgba(255,255,255,.62)}.about-timeline{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin-top:28px;counter-reset:about-step}.about-step{position:relative;padding:24px 20px 22px;border-radius:20px;background:#0b0b0b;border:1px solid rgba(255,255,255,.13)}.about-step:before{counter-increment:about-step;content:"0" counter(about-step);display:block;margin-bottom:22px;color:#cef16c;font-size:13px;font-weight:700;letter-spacing:.08em}.about-step strong{display:block;font-size:19px;line-height:1.22;margin-bottom:8px}.about-step span{color:rgba(255,255,255,.58);font-size:15px;line-height:1.5}.about-articles{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin-top:28px}.about-article{display:flex;flex-direction:column;min-height:220px;padding:22px;border:1px solid rgba(255,255,255,.14);border-radius:20px;background:rgba(255,255,255,.045);color:#fff;text-decoration:none;transition:border-color .2s,transform .2s}.about-article:hover{border-color:rgba(206,241,108,.5);transform:translateY(-2px)}.about-article small{color:#cef16c;text-transform:uppercase;letter-spacing:.08em;font-weight:700}.about-article strong{display:block;margin:18px 0;font-size:19px;line-height:1.32}.about-article span{margin-top:auto;color:rgba(255,255,255,.5);font-size:14px}.about-cta{display:flex;align-items:center;justify-content:space-between;gap:28px;margin:58px 0 18px;padding:30px;border-radius:24px;background:#cef16c;color:#080808}.about-cta h2{font-size:clamp(26px,4vw,40px);margin:0 0 8px}.about-cta p{margin:0;color:rgba(0,0,0,.7)}.about-cta .btn{flex:0 0 auto;margin:0;background:#080808;color:#fff}.about-footer{width:min(1040px,calc(100% - 36px));margin:auto}@media(max-width:760px){.about-hero{grid-template-columns:1fr;padding-top:38px}.about-hero-copy{order:1}.about-photo-wrap{order:2;max-width:520px}.about-principles,.about-timeline,.about-articles{grid-template-columns:1fr}.about-article{min-height:0}.about-cta{align-items:flex-start;flex-direction:column}.about-section{padding:40px 0}}@media(max-width:420px){.about-wrap,.about-footer{width:min(100% - 30px,1040px)}.about-hero h1{font-size:40px}.about-photo{border-radius:24px}.about-quote{padding:20px}.about-cta{padding:24px}}
.about-section{padding:64px 0}.about-section-label{margin:0 0 12px;color:#cef16c;font-size:12px;font-weight:750;letter-spacing:.12em;text-transform:uppercase}.about-section h2{font-size:clamp(32px,5vw,50px);line-height:1.02;letter-spacing:-.035em;margin-bottom:24px}.about-quote{position:relative;margin-top:36px;padding:28px 32px 28px 42px;border-color:rgba(206,241,108,.26)}.about-quote:before{content:"";position:absolute;left:22px;top:29px;bottom:29px;width:3px;border-radius:3px;background:#cef16c}.about-principles{gap:14px;margin-top:32px}.about-principle{position:relative;overflow:hidden;min-height:184px;padding:24px;border-radius:22px;background:linear-gradient(145deg,rgba(255,255,255,.065),rgba(255,255,255,.025))}.about-principle:after{content:"";position:absolute;right:-54px;bottom:-74px;width:150px;height:150px;border-radius:50%;background:radial-gradient(circle,rgba(206,241,108,.11),transparent 68%)}.about-principle-mark{display:block;margin-bottom:38px;color:#cef16c;font-size:12px;font-weight:750;letter-spacing:.1em}.about-principle b{margin-bottom:10px;font-size:19px;line-height:1.2}.about-principle p{position:relative;z-index:1;line-height:1.55}.about-timeline{position:relative;gap:22px;margin-top:34px}.about-timeline:before{content:"";position:absolute;left:17px;right:17px;top:17px;height:1px;background:linear-gradient(90deg,#cef16c,rgba(206,241,108,.34),rgba(255,255,255,.12))}.about-step{padding:0 22px 0 0;border:0;border-radius:0;background:transparent}.about-step:before{position:relative;z-index:1;display:grid;place-items:center;width:34px;height:34px;margin-bottom:24px;border:1px solid rgba(206,241,108,.56);border-radius:50%;background:#080808;font-size:11px;font-weight:750}.about-step strong{font-size:20px;margin-bottom:10px}.about-step span{line-height:1.55}.about-articles{gap:14px;margin-top:32px}.about-article{position:relative;min-height:244px;padding:24px;border-radius:22px;background:linear-gradient(150deg,rgba(113,55,220,.12),rgba(255,255,255,.035) 46%,rgba(255,255,255,.02));transition:border-color .2s,transform .2s,background .2s}.about-article:after{content:"↗";position:absolute;top:20px;right:22px;color:rgba(255,255,255,.42);font-size:20px}.about-article:hover{background:linear-gradient(150deg,rgba(113,55,220,.18),rgba(255,255,255,.055));transform:translateY(-3px)}.about-article strong{margin:42px 0 20px;line-height:1.34}.about-cta{margin-top:64px;padding:32px;border-radius:26px;box-shadow:0 24px 70px rgba(206,241,108,.12)}.about-cta h2{line-height:1.05;letter-spacing:-.035em}.about-cta .btn{transition:transform .2s}.about-cta .btn:hover{transform:translateY(-2px)}.about-main a:focus-visible,header a:focus-visible,footer a:focus-visible{outline:2px solid #cef16c;outline-offset:4px}@media(max-width:760px){.about-timeline{gap:0;margin-left:2px}.about-timeline:before{left:17px;right:auto;top:17px;bottom:24px;width:1px;height:auto;background:linear-gradient(#cef16c,rgba(206,241,108,.28),rgba(255,255,255,.1))}.about-step{padding:0 0 30px 58px}.about-step:before{position:absolute;left:0;top:0}.about-step:last-child{padding-bottom:0}.about-article{min-height:190px}.about-section{padding:48px 0}}@media(max-width:420px){.about-quote{padding:22px 24px 22px 36px}.about-quote:before{left:18px;top:23px;bottom:23px}}@media(prefers-reduced-motion:reduce){.about-article,.about-cta .btn{transition:none}}
.about-caption span{display:block}.about-caption span+span{margin-top:2px}
""".strip()

JS = r"""(function(){
  var METRIKA_ID=112705935;
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
    var dl=e.target.closest&&e.target.closest('a.js-download');
    if(dl){goal('template_download',{page:location.pathname});return;}
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
})();""".strip()

SOURCES = [
    ("Банк России: финансовая грамотность и защита потребителей", "https://cbr.ru/protection_rights/finprosvet/"),
    ("Финансовая культура Банка России: личный бюджет и накопления", "https://fincult.info/"),
]

PAGES = {
"kontrol-finansov": {
 "title":"Контроль финансов: как держать расходы и бюджет под контролем",
 "desc":"Практичная система контроля личных финансов: обязательные расходы, свободный остаток, цели и регулярная проверка без сложных таблиц.",
 "h1":"Как контролировать личные финансы без ежедневной бухгалтерии",
 "lead":"Контроль финансов — это не запрет на покупки. Это понятный ответ на три вопроса: сколько уже обязано уйти, сколько можно потратить сейчас и что изменится после покупки.",
 "answer":"Начните не с категорий, а с календаря денег: доход → обязательные платежи → цели → свободный остаток. Затем пересчитывайте остаток после каждой заметной траты.",
 "sections":[("Что именно контролировать",["До следующего дохода важнее всего видеть обязательные платежи с датами, текущий свободный остаток и цели, которые вы не хотите сдвигать.","Категории полезны для анализа, но сами по себе не отвечают, можно ли сегодня потратить 2 000 ₽ без последствий."]), ("Простая система из четырёх шагов",["Запишите ближайший доход и дату.","Вычтите аренду, кредиты, связь, подписки и другие обязательные платежи до этой даты.","Отдельно зарезервируйте сумму на финансовые цели.","Остаток считайте деньгами на повседневные траты и пересчитывайте после покупок."]), ("Когда нужен анализ расходов",["Если денег регулярно не хватает до зарплаты, сравните не отдельные покупки, а повторяющиеся группы расходов за несколько периодов. Ищите один-два крупных рычага, а не десятки мелких запретов."])],
 "faq":[("Как часто проверять бюджет?","Достаточно после крупных трат и при изменении обязательных платежей. Смысл контроля — держать план актуальным, а не увеличивать число проверок."),("Нужен ли доступ к банковскому счёту?","Нет. Для базового контроля достаточно вручную или по скриншоту обновлять фактические траты и остаток.")],
 "related":["tablica-dohodov-i-rashodov","planirovanie-byudzheta","prilozhenie-dlya-kontrolya-rashodov"]},
"analiz-rashodov": {
 "title":"Анализ расходов: как понять, куда уходят деньги",
 "desc":"Пошаговый анализ личных расходов: как найти повторяющиеся траты, сравнить периоды и выбрать изменения, которые реально влияют на бюджет.",
 "h1":"Как анализировать расходы и не утонуть в категориях",
 "lead":"Хороший анализ расходов заканчивается решением. Если после красивой диаграммы непонятно, что изменить в следующем месяце, она не выполнила задачу.",
 "answer":"Сначала сравните общий расход и 5–7 крупных групп за несколько периодов. Затем выберите максимум два изменения, которые дают заметный эффект без постоянного самоконтроля.",
 "sections":[("С чего начать",["Сведите фактические траты за одинаковые интервалы: например, три полных месяца. Разовые крупные покупки пометьте отдельно, чтобы они не маскировали обычный уровень расходов."]), ("Ищите структуру, а не виноватых",["Отдельно посмотрите жильё, транспорт, продукты, кафе, сервисы и прочие крупные группы. Рост одной категории может быть нормальным, если изменились обстоятельства."]), ("Переведите вывод в правило",["Вместо «меньше тратить» сформулируйте конкретное изменение: пересмотреть один тариф, заранее задать недельный лимит на кафе или перенести цель на реальную дату."])],
 "faq":[("Сколько категорий нужно?","Столько, чтобы видеть крупные причины изменений. Для большинства задач десятки микрокатегорий не обязательны."),("Как понять, что расход слишком большой?","Сравнивайте его с собственными обязательствами, доходом и целями. Универсальная доля подходит не всем.")],
 "related":["tablica-dohodov-i-rashodov","kak-ekonomit-dengi","kontrol-finansov"]},
"planirovanie-byudzheta": {
 "title":"Планирование бюджета на месяц: простой план от зарплаты до зарплаты",
 "desc":"Как составить личный или семейный бюджет на месяц: доходы, обязательные платежи, накопления, переменные траты и пересчёт после изменений.",
 "h1":"Как составить бюджет на месяц и не забыть про жизнь между таблицами",
 "lead":"Рабочий бюджет — не прогноз до рубля. Это порядок, в котором деньги получают задачи: обязательное, цели и только потом свободные траты.",
 "answer":"Составьте календарь доходов и обязательных платежей, зарезервируйте цели, а свободный остаток распределите на период до следующего дохода. При изменении факта пересчитайте план.",
 "sections":[("Личный бюджет",["Начните с денег, которые реально будут доступны в периоде, а не со средней зарплаты за год. Затем внесите платежи с датой и сумму на цели."]), ("Семейный бюджет",["Если расходы общие, удобнее сначала считать общий обязательный контур семьи, а уже затем личные суммы каждого. Важно заранее договориться, какие траты считаются общими."]), ("Почему бюджет ломается",["Чаще всего план устаревает после первой внеплановой покупки. Не пытайтесь сохранить первоначальные цифры — пересчитайте остаток и следующие решения."])],
 "faq":[("Нужно ли планировать весь месяц, если зарплата два раза?","Лучше строить периоды между фактическими поступлениями денег. Так обязательства и свободный остаток видны точнее."),("Как учесть нерегулярный доход?","Планируйте только уже полученную или достаточно надёжно ожидаемую сумму и не занимайте будущий доход заранее.")],
 "related":["kak-raspredelit-zarplatu","kontrol-finansov","planirovshchik-byudzheta"]},
"kak-raspredelit-zarplatu": {
 "title":"Как распределить зарплату на месяц: обязательное, цели и свободные деньги",
 "desc":"Понятный способ распределить зарплату: сначала платежи до следующего дохода, затем накопления и только после этого доступная сумма на жизнь.",
 "h1":"Как распределить зарплату, чтобы не занимать у себя из будущего",
 "lead":"Проценты вроде 50/30/20 удобны как ориентир, но реальный план начинается с ваших дат и сумм. Аренда и кредит не становятся меньше только потому, что не вписались в универсальную схему.",
 "answer":"В день дохода зарезервируйте обязательные платежи до следующего поступления, затем сумму на важные цели. Остаток — это бюджет повседневных решений на этот период.",
 "sections":[("Шаг 1. Защитите обязательное",["Соберите все платежи с датой до следующей зарплаты. Эти деньги лучше мысленно исключить из доступного остатка сразу."]), ("Шаг 2. Заплатите будущему себе",["Определите реалистичную сумму на подушку или цель. Если она постоянно заставляет занимать до зарплаты, план нужно уменьшить, а не скрывать кассовый разрыв."]), ("Шаг 3. Разделите свободный остаток",["Можно использовать дневной или недельный ориентир. После крупной покупки пересчитайте остаток на оставшиеся дни."])],
 "faq":[("Работает ли правило 50/30/20?","Это ориентир, а не обязательный норматив. При высокой аренде, долгах или нестабильном доходе фактическая структура будет другой."),("Когда откладывать на цели?","Лучше резервировать сумму сразу после дохода, но только в размере, который не создаёт новый долг до следующего поступления.")],
 "related":["planirovanie-byudzheta","kak-kopit-dengi","skolko-mozhno-tratit"]},
"kak-ekonomit-dengi": {
 "title":"Как экономить деньги без постоянных запретов",
 "desc":"Как научиться экономить и меньше тратить: найти крупные повторяющиеся расходы, задать ориентир и сохранить важные покупки в бюджете.",
 "h1":"Как меньше тратить и не превратить экономию в наказание",
 "lead":"Экономия работает дольше, когда убирает автоматические лишние расходы, а не требует каждый день побеждать себя возле кофейни.",
 "answer":"Ищите повторяющиеся расходы с заметной суммой, меняйте один-два правила за раз и заранее оставляйте деньги на то, от чего не хотите отказываться.",
 "sections":[("Начните с крупных рычагов",["Проверьте тарифы, подписки, доставку, транспорт и привычные сценарии покупок. Один повторяющийся расход часто важнее десятка разовых мелочей."]), ("Сделайте ограничение видимым",["Недельный ориентир проще контролировать, чем абстрактное «буду тратить меньше». Он должен учитывать уже зарезервированные обязательства."]), ("Не экономьте за счёт будущего",["Если сокращение трат ведёт к тому, что позже приходится закрывать базовые расходы кредитом, такая экономия неустойчива."])],
 "faq":[("С чего начать экономить?","С анализа повторяющихся крупных трат и расходов, которые почти не дают ценности. Не обязательно начинать с самых частых мелких покупок."),("Как экономить, если доход небольшой?","Сначала защитите базовые обязательства и избегайте советов с фиксированными процентами. При маленьком остатке задача может быть не в сокращении, а в предотвращении кассовых разрывов.")],
 "related":["analiz-rashodov","kak-raspredelit-zarplatu","kak-kopit-dengi"]},
"kak-kopit-dengi": {
 "title":"Как копить деньги: план накоплений, который учитывает обычные траты",
 "desc":"Как начать копить деньги на цель: определить сумму и срок, посчитать взнос, проверить нагрузку на бюджет и корректировать план без чувства провала.",
 "h1":"Как копить деньги, когда жизнь продолжает стоить денег",
 "lead":"Накопление становится планом, когда у цели есть сумма, срок и посильный регулярный взнос. Всё остальное — пожелание, которое первым проигрывает неожиданной покупке.",
 "answer":"Определите цель и срок, разделите недостающую сумму на число периодов и проверьте, остаётся ли после взноса достаточно на обязательные и повседневные расходы.",
 "sections":[("Сделайте цель измеримой",["Формулировка «копить больше» не даёт действия. Нужны сумма, текущий остаток и желаемая дата."]), ("Проверьте темп",["Если требуемый ежемесячный взнос ломает бюджет, меняйте срок или сумму цели до начала накопления. Нереалистичный план не становится дисциплиной от того, что записан в приложении."]), ("Отделите цель от подушки",["Резерв на непредвиденные базовые расходы и покупка на конкретную дату решают разные задачи. Не стоит считать одни и те же деньги одновременно и подушкой, и первоначальным взносом."])],
 "faq":[("Как начать копить с нуля?","Выберите одну небольшую понятную цель и посильный автоматический или регулярный взнос. Сначала важнее повторяемость, чем максимальная сумма."),("Что делать, если пришлось взять деньги из накоплений?","Обновите фактический остаток и пересчитайте срок или следующий взнос. Это изменение плана, а не причина перестать копить.")],
 "related":["kalkulyator-nakopleniy","finansovye-celi","finansovaya-podushka"]},
"finansovye-celi": {
 "title":"Финансовые цели: как поставить срок и не конфликтовать с бюджетом",
 "desc":"Как превратить финансовую цель в план: сумма, срок, приоритет, регулярный взнос и пересчёт при изменениях доходов или расходов.",
 "h1":"Финансовые цели, которые помещаются в реальную жизнь",
 "lead":"Цель конкурирует не с силой воли, а с другими задачами денег. Поэтому ей нужен приоритет и понятный взнос, который не уничтожает бюджет до зарплаты.",
 "answer":"Для каждой цели задайте сумму, дату и текущий накопленный остаток. Затем посчитайте взнос и сравните несколько целей по приоритету вместо попытки финансировать все одинаково.",
 "sections":[("Одна цель — три числа",["Целевая сумма, дата и уже накопленное. Этого достаточно, чтобы увидеть требуемый темп и понять, реалистичен ли он."]), ("Приоритет важнее количества",["Если одновременно копить на отпуск, машину и подушку одинаковыми долями, ни одна цель может не двигаться заметно. Расставьте порядок и минимальные взносы."]), ("Пересмотр — часть плана",["Изменение срока после падения дохода или роста обязательных расходов — нормальная финансовая корректировка, а не провал."])],
 "faq":[("Сколько финансовых целей вести одновременно?","Столько, сколько можно финансировать без кассового разрыва. Практически проще видеть несколько приоритетов, чем длинный список без движения."),("Нужно ли учитывать инфляцию?","Для долгих целей полезно периодически пересматривать целевую сумму по фактической цене нужной покупки. Необязательно угадывать точный процент на годы вперёд.")],
 "related":["kak-kopit-dengi","kalkulyator-nakopleniy","kak-nakopit-na-kvartiru"]},
"kalkulyator-nakopleniy": {
 "title":"Калькулятор накоплений: сколько откладывать в месяц на цель",
 "desc":"Калькулятор накоплений: цель, уже накопленная сумма и срок. Покажет простой ежемесячный взнос без предположений о доходности.",
 "h1":"Калькулятор накоплений на цель",
 "lead":"Введите сумму цели, сколько уже есть и число месяцев. Калькулятор покажет базовый взнос без учёта процентов и инвестиционной доходности — только прозрачная арифметика.",
 "answer":"Формула: (целевая сумма − уже накоплено) ÷ число месяцев. Если результат не помещается в бюджет, меняйте срок или размер цели.",
 "tool":"savings",
 "sections":[("Как читать результат",["Это не прогноз инвестиционной доходности и не обещание результата. Это минимальная арифметическая скорость накопления при равных взносах."]), ("Проверьте бюджет до старта",["Сумма взноса должна оставлять деньги на обязательные платежи и нормальные повседневные расходы. Иначе план будет регулярно срываться."])],
 "faq":[("Учитывает ли калькулятор проценты?","Нет. Специально: результат не зависит от предположений о ставке или доходности и показывает только нужный собственный взнос."),("Что если срок не целое число месяцев?","Возьмите ближайшее удобное число периодов и пересчитайте план при приближении к цели.")],
 "related":["kak-kopit-dengi","finansovye-celi","kak-nakopit-na-kvartiru"]},
"kalkulyator-finansovoy-podushki": {
 "title":"Калькулятор финансовой подушки: размер резерва по вашим расходам",
 "desc":"Калькулятор финансовой подушки: укажите обязательные расходы и число месяцев резерва, чтобы получить ориентир суммы без универсальных процентов от дохода.",
 "h1":"Калькулятор размера финансовой подушки",
 "lead":"Размер резерва логичнее считать от необходимых расходов, а не от зарплаты: именно эти траты придётся продолжать при временном падении дохода.",
 "answer":"Укажите обязательные расходы за месяц и желаемое число месяцев автономности. Получившаяся сумма — ориентир, который стоит адаптировать к стабильности дохода и семейной ситуации.",
 "tool":"cushion",
 "sections":[("Что включать в обязательные расходы",["Жильё, базовые продукты, лекарства, транспорт, связь, обязательные платежи по долгам и другие расходы, которые нельзя быстро убрать."]), ("Почему нет одного правильного числа месяцев",["Риск потери дохода, число источников дохода, наличие иждивенцев и доступность страховок различаются. Калькулятор поэтому позволяет выбрать горизонт самостоятельно."])],
 "faq":[("Подушка и накопления на отпуск — одно и то же?","Нет. Подушка нужна для непредвиденного падения дохода или обязательных расходов, а отпуск — плановая цель с датой."),("Где хранить подушку?","Критерии резерва — доступность и низкий риск потери средств. Конкретный финансовый продукт зависит от вашей ситуации и условий организаций.")],
 "related":["finansovaya-podushka","kak-kopit-dengi","finansovyy-stress"]},
"kak-nakopit-na-kvartiru": {
 "title":"Как накопить на квартиру: план первоначального взноса без магических процентов",
 "desc":"Как составить план накопления на квартиру или первоначальный взнос: целевая сумма, срок, ежемесячный взнос, резерв и контроль прогресса.",
 "h1":"Как накопить на квартиру: превратить большую сумму в понятный маршрут",
 "lead":"Большая цель становится управляемой, когда отделена от подушки и разбита на регулярный взнос. Начните с фактической цены цели, а не с процента от зарплаты.",
 "answer":"Определите сумму собственного взноса и сопутствующих расходов, вычтите уже накопленное, задайте срок и посчитайте требуемый ежемесячный темп. Затем проверьте его на вашем бюджете.",
 "sections":[("Считайте всю цель",["Кроме самого взноса могут быть расходы на переезд, оформление, ремонт и базовое обустройство. Необязательно угадывать их точно, но лучше иметь отдельный резерв."]), ("Не отдавайте подушку целиком",["После крупной покупки доходы и обязательства никуда не исчезают. Если весь резерв превращается в взнос, любой сбой после сделки становится дорогим."]), ("Пересматривайте цену",["Для цели на несколько лет полезно периодически обновлять фактическую стоимость подходящих вариантов и целевую сумму, а не держаться за старую цифру."])],
 "faq":[("С чего начать накопление на квартиру?","С определения конкретной суммы собственного капитала и срока. После этого становится виден требуемый взнос и можно оценить реалистичность плана."),("Стоит ли копить одновременно на ремонт?","Если ремонт почти неизбежен, лучше учитывать его как отдельную подцель, чтобы после покупки не финансировать всё из аварийного резерва.")],
 "related":["kalkulyator-nakopleniy","finansovye-celi","finansovaya-podushka"]},
"kak-nakopit-na-mashinu": {
 "title":"Как накопить на машину: сумма, срок и ежемесячный план",
 "desc":"План накопления на автомобиль: как учесть стоимость покупки, стартовые расходы, текущие накопления и реальный ежемесячный взнос.",
 "h1":"Как накопить на машину и не забыть о расходах после покупки",
 "lead":"Цена автомобиля — не вся цель. Страхование, регистрация, обслуживание и сезонные расходы появляются сразу после покупки, поэтому резерв лучше заложить заранее.",
 "answer":"Выберите реалистичную цену машины, добавьте стартовый резерв, вычтите уже накопленное и разделите остаток на срок. Затем сравните взнос со свободным остатком бюджета.",
 "sections":[("Соберите целевую сумму",["Отдельно запишите цену автомобиля и расходы первого периода. Это помогает не потратить весь капитал в день покупки."]), ("Сравнивайте сценарии",["Посчитайте два-три срока: например, быстрее с большим взносом и спокойнее с меньшим. Решение становится понятнее, когда видно цену каждого сценария в месяц."]), ("После покупки бюджет изменится",["Транспортные расходы не заканчиваются на цене автомобиля. Проверьте, как регулярные траты впишутся в обычный месяц."])],
 "faq":[("Нужно ли учитывать продажу текущей машины?","Да, но консервативно: используйте сумму, которую реально ожидаете получить, и обновите расчёт после продажи."),("Кредит или накопление?","Это уже индивидуальное финансовое решение с ценой кредита и рисками. Эта страница помогает посчитать собственный капитал и темп накопления, а не выбрать кредит.")],
 "related":["kalkulyator-nakopleniy","kak-kopit-dengi","planirovanie-byudzheta"]},
"kak-nakopit-na-otpusk": {
 "title":"Как накопить на отпуск: бюджет поездки и взнос по месяцам",
 "desc":"Как накопить на отпуск без кассового разрыва: посчитать полный бюджет поездки, срок, ежемесячный взнос и запас на изменение цены.",
 "h1":"Как накопить на отпуск заранее, а не оплачивать его после возвращения",
 "lead":"У отпуска есть дата, поэтому это удобная финансовая цель: можно посчитать темп заранее и увидеть, нужно ли менять бюджет поездки или срок накопления.",
 "answer":"Сложите транспорт, жильё, ежедневные траты, страховку и запас; вычтите уже накопленное и разделите остаток на количество месяцев до поездки.",
 "sections":[("Считайте полную поездку",["Билеты и отель — только часть стоимости. Добавьте питание, местный транспорт, связь, страховку и разумный запас."]), ("Резервируйте постепенно",["Регулярный взнос снижает вероятность, что отпуск конкурирует с арендой и другими обязательствами в одном месяце."]), ("Обновляйте бюджет",["Если билеты или курс валют заметно изменились, пересчитайте цель сразу, а не в последнюю неделю."])],
 "faq":[("Сколько закладывать на непредвиденное?","Универсального процента нет. Добавьте отдельный резерв, исходя из неопределённости цен и возможности быстро изменить поездку."),("Можно ли использовать подушку на отпуск?","По смыслу лучше разделять: отпуск — плановая цель, а подушка нужна для непредвиденных базовых проблем.")],
 "related":["kalkulyator-nakopleniy","finansovye-celi","kak-ekonomit-dengi"]},
"kak-nakopit-na-telefon": {
 "title":"Как накопить на телефон: быстрый план без рассрочки",
 "desc":"Как посчитать накопление на новый телефон: выбрать бюджет покупки, срок и еженедельный или ежемесячный взнос без ущерба обязательным расходам.",
 "h1":"Как накопить на телефон и понять, сколько откладывать",
 "lead":"Небольшую по сравнению с квартирой цель удобно использовать как тренировку финансового планирования: сумма понятна, срок короткий, результат легко проверяется.",
 "answer":"Задайте максимальный бюджет покупки, вычтите уже накопленное и разделите остаток на число недель или месяцев. Не увеличивайте взнос за счёт обязательных платежей.",
 "sections":[("Ограничьте бюджет до выбора модели",["Сначала определите сумму, которую готовы направить на покупку, и только потом сравнивайте устройства. Иначе цель растёт вместе с витриной."]), ("Сделайте короткий график",["Для короткой цели недельный взнос иногда нагляднее месячного. Главное — чтобы общий темп совпадал с датой покупки."]), ("Оставьте место обычным тратам",["Если цель требует отказаться от базовых расходов или залезать в долг к концу месяца, увеличьте срок."])],
 "faq":[("Что делать со старым телефоном?","Если планируете продать его, добавляйте ожидаемую сумму в расчёт консервативно и окончательно пересчитайте цель после продажи."),("Стоит ли брать рассрочку вместо накопления?","Это зависит от условий договора и вашего бюджета. Здесь считается только сценарий накопления собственных денег.")],
 "related":["kalkulyator-nakopleniy","kak-kopit-dengi","kak-ekonomit-dengi"]},
"kak-nakopit-na-svadbu": {
 "title":"Как накопить на свадьбу: план бюджета и взносов до даты",
 "desc":"Как накопить на свадьбу: определить бюджет, разделить обязательные и желательные расходы, посчитать регулярный взнос и запас до даты события.",
 "h1":"Как накопить на свадьбу без финансового похмелья после праздника",
 "lead":"У свадьбы фиксированная дата и много переменных расходов. Поэтому полезно разделить «обязательно» и «хочется», чтобы цель не росла незаметно по мере подготовки.",
 "answer":"Соберите базовый бюджет, добавьте резерв, вычтите уже накопленное и разделите остаток на месяцы до даты. Все новые идеи добавляйте в смету вместе с источником денег.",
 "sections":[("Разделите бюджет на уровни",["Сначала обязательная часть: площадка, документы, базовая логистика. Затем желательные элементы, которые можно менять без срыва события."]), ("Синхронизируйте общий план",["Если копят двое, договоритесь о суммах и датах взносов. Общая цель без понятной ответственности часто превращается в расчёт «кто сколько уже потратил» после факта."]), ("Не считайте подарки источником оплаты",["Подарки неизвестны до события, поэтому безопаснее не финансировать ими уже заключённые обязательства."])],
 "faq":[("Как сократить бюджет свадьбы?","Сравнивайте не мелочи, а крупные блоки сметы и количество гостей: именно они обычно сильнее всего меняют итоговую сумму."),("Нужен ли отдельный резерв?","Полезно оставить запас на изменения цены и мелкие расходы последних недель, но его размер зависит от конкретной сметы.")],
 "related":["kalkulyator-nakopleniy","finansovye-celi","planirovanie-byudzheta"]},
"prilozhenie-dlya-kontrolya-rashodov": {
 "title":"Приложение для контроля расходов: что должно помогать, а не отвлекать",
 "desc":"Как выбрать приложение для контроля расходов и бюджета: быстрый ввод, обязательные платежи, план до зарплаты, цели и понятный пересчёт после покупок.",
 "h1":"Как выбрать приложение для контроля расходов и бюджета",
 "lead":"Лучший финансовый трекер — не тот, где больше графиков, а тот, который помогает принять следующее решение и не требует поддерживать идеальную бухгалтерию.",
 "answer":"Проверьте четыре вещи: насколько быстро вносится факт, видны ли обязательные платежи, пересчитывается ли доступная сумма после трат и можно ли держать цели отдельно от свободных денег.",
 "sections":[("Учёт — только первый слой",["Категории показывают прошлое. Для повседневного решения важнее связать факт с тем, сколько осталось до следующего дохода и какие платежи ещё впереди."]), ("Автоматизация не обязана означать доступ к банку",["Некоторым удобна банковская синхронизация, другим — ручной ввод или распознавание скриншота. Выбирайте способ, который не вызывает недоверия и реально будет использоваться."]), ("Что делает Кубыш",["Кубыш строит маршрут между получками: учитывает обязательные платежи и цели, показывает сумму на сегодня и пересчитывает её после новых трат. Банковский доступ для базового сценария не нужен."])],
 "faq":[("Нужен ли финансовому приложению доступ ко всем счетам?","Не обязательно. Ручной ввод или импорт факта может быть достаточен, если вам важнее план до следующего дохода, а не автоматическая полная выписка."),("Чем планировщик отличается от учёта расходов?","Учёт фиксирует прошлое; планировщик связывает будущие доходы, обязательства и цели с доступной суммой на текущие решения.")],
 "related":["kontrol-finansov","planirovshchik-byudzheta","tablica-dohodov-i-rashodov"]},
"planirovshchik-byudzheta": {
 "title":"Планировщик бюджета: как выбрать систему для личных финансов",
 "desc":"Планировщик бюджета должен связывать доходы, обязательные платежи, цели и фактические траты. Чек-лист функций и простой способ начать.",
 "h1":"Планировщик бюджета, который не устаревает после первой покупки",
 "lead":"Статичный бюджет быстро расходится с реальностью. Полезный планировщик должен не хранить первоначальный план как музейный экспонат, а пересчитывать следующие решения после факта.",
 "answer":"Ищите систему, где есть даты доходов и обязательных платежей, цели, фактические траты и автоматический пересчёт свободного остатка на оставшийся период.",
 "sections":[("Что должно быть в основе",["Календарь денежных событий важнее длинного списка категорий: когда придёт доход, когда спишется обязательное, сколько уже зарезервировано на цели."]), ("Как начать за 15 минут",["Добавьте ближайший доход, 5–10 обязательных платежей и одну главную цель. После этого уже можно считать реальный свободный остаток, а детализацию наращивать позже."]), ("Не делайте второй проект из бюджета",["Если система требует часов поддержки каждую неделю, она конкурирует с задачей, которую должна облегчать. Упрощайте ввод до устойчивого уровня."])],
 "faq":[("Нужен ли Excel?","Таблица подходит, если вам комфортно пересчитывать её вручную. Приложение полезнее, когда важно обновлять план сразу после фактических трат."),("Что важнее: категории или календарь?","Для ответа «хватит ли до зарплаты» календарь обязательных платежей и доходов обычно важнее подробной категоризации прошлого.")],
 "related":["planirovanie-byudzheta","prilozhenie-dlya-kontrolya-rashodov","kontrol-finansov"]},
"finansovyy-stress": {
 "title":"Финансовый стресс: как вернуть ощущение контроля над деньгами",
 "desc":"Практические шаги при финансовом стрессе: собрать обязательства, увидеть ближайший горизонт, отделить факты от неопределённости и составить короткий план.",
 "h1":"Что делать, когда деньги постоянно держат в напряжении",
 "lead":"Финансовый стресс часто усиливается не только из-за суммы денег, но и из-за неопределённости: непонятно, что уже обязательно, сколько свободно и какой платёж следующий.",
 "answer":"Сузьте горизонт до следующего дохода: выпишите доступные деньги, обязательные платежи и даты. Сначала восстановите видимость ближайшего периода, а уже потом решайте долгие цели.",
 "sections":[("Уберите неизвестные из ближайших недель",["Список обязательных платежей и реального остатка не решает все проблемы, но превращает часть тревоги в конкретные задачи с датами."]), ("Разделите срочное и важное",["Просрочка обязательного платежа и желание быстрее накопить на цель — разные приоритеты. При дефиците сначала защищайте базовые обязательства."]), ("Когда нужна помощь",["Если долги растут, есть риск пропустить платежи или тревога заметно мешает повседневной жизни, стоит обратиться за персональной помощью к подходящему специалисту. Общая статья не заменяет консультацию."])],
 "faq":[("Поможет ли бюджет убрать тревогу?","Он не лечит тревожное состояние, но может снизить неопределённость: видно ближайшие обязательства и доступный остаток."),("Что делать, если расходов больше дохода?","Сначала зафиксировать дефицит без самообмана, расставить обязательства по срочности и искать крупные изменения доходов/расходов. Для долговых решений лучше получить персональную консультацию.")],
 "related":["kontrol-finansov","planirovanie-byudzheta","finansovaya-podushka"]},
}

# A single month-budget page covers the closely related "личный бюджет" and
# "семейный бюджет" formulations without creating near-duplicate doorways.
PAGES["byudzhet-na-mesyats"] = {
 "title":"Личный и семейный бюджет на месяц: пример структуры",
 "desc":"Как спланировать личный или семейный бюджет на месяц: общий доход, обязательные расходы, цели, личные суммы и свободный остаток.",
 "h1":"Личный и семейный бюджет на месяц: одна структура, разные договорённости",
 "lead":"Формула бюджета одинаковая: доступные доходы минус обязательства и цели. В семье добавляется ещё один слой — договорённость, какие деньги и расходы общие.",
 "answer":"Сведите доходы периода, внесите общие обязательные платежи, зафиксируйте цели и только затем определите свободный остаток и личные суммы каждого.",
 "sections":[("Личный бюджет",["Работайте с периодом между доходами: так не придётся искусственно растягивать деньги на календарный месяц, если поступления идут в другие даты."]), ("Семейный бюджет",["Сначала договоритесь о принципе: общий котёл, пропорциональные взносы или фиксированные зоны ответственности. Самая точная таблица не заменит эту договорённость."]), ("Обновляйте после факта",["Покупка, перенос платежа или изменение дохода должны менять остаток. Бюджет полезен как живая модель, а не как обещание самому себе первого числа."])],
 "faq":[("Нужно ли объединять все деньги в семье?","Нет. Важно не конкретное устройство счетов, а чтобы общие обязательства и правила их финансирования были прозрачны обоим."),("Что делать с нерегулярными расходами?","Заранее создавать для крупных предсказуемых расходов отдельные цели/резервы и не считать эти деньги свободными.")],
 "related":["planirovanie-byudzheta","kak-raspredelit-zarplatu","kontrol-finansov"]}


PAGES["prilozhenie-kopilka"] = {
 "published":"2026-10-05", "modified":"2026-10-05",
 "title":"Приложение-копилка для iPhone: сумма в месяц и дата для каждой цели",
 "desc":"Приложение-копилка для iPhone: несколько целей на одном счете, сумма в месяц и дата для каждой, подбор вкладов под сроки целей. Без подключения банка.",
 "h1":"Приложение-копилка для iPhone, которое показывает, когда вы накопите",
 "lead":"Обычная копилка хранит деньги. Хорошая показывает, сколько откладывать с каждой зарплаты и когда цель станет реальной. Разбираем, что должно уметь приложение-копилка и как копить на несколько целей сразу.",
 "answer":"Выбирайте копилку, которая считает от вашей зарплаты, а не просто складывает суммы. Она должна показывать взнос в месяц, дату для каждой цели и что станет с целями после крупной покупки.",
 "app":{"title":"Кубыш: копилка, которая считает за вас","img":"goals-1-7.webp","alt":"Цели в Кубыше: накоплено, сумма в месяц и дата для каждой цели",
        "points":["Несколько целей на одном счете: подушка, отпуск, телефон, машина","Сумма в месяц и дата для каждой цели","С каждой получки Кубыш предлагает, сколько отложить, и показывает бюджет на день","Подбирает выгодные вклады и накопительные счета под сроки целей","Траты скриншотом из банка, подключать банк не нужно"]},
 "tool":"savings",
 "sections":[
  ("Чем приложение-копилка отличается от копилки в банке",["Банковские копилки обычно работают по одному правилу: округляют покупки или переводят процент от поступлений. Деньги копятся, но непонятно, на что они и к какой дате их хватит.","Приложение-копилка работает от цели. Вы задаете сумму и срок, а оно считает, сколько откладывать с каждой зарплаты и успеваете ли вы. Эти два подхода не мешают друг другу: деньги могут лежать в банке, а план держит приложение."]),
  ("Что должно уметь приложение-копилка",["Считать от зарплаты. Если зарплата приходит 10-го и 25-го, план должен строиться по этим датам, а не по календарному месяцу.","Держать несколько целей сразу и говорить, какая идет первой. Иначе подушка, отпуск и новый телефон спорят за одни и те же деньги.","Показывать дату. Сумма «накоплено 40%» мотивирует слабее, чем «отпуск будет в июле, если откладывать 6 000 в месяц».","Пересчитывать после покупок. Крупная трата сдвигает цели, и об этом лучше узнать до покупки, а не через месяц.","Не требовать доступ к банку. Для копилки хватает суммы зарплаты, обязательных платежей и целей."]),
  ("Пример: две цели с зарплаты 80 000 ₽",["Обязательные платежи (аренда, связь, кредит) занимают 35 000 ₽. На жизнь до следующей получки оставляем 30 000 ₽. На цели остается 15 000 ₽ в месяц.","Подушка безопасности на 180 000 ₽ идет первой: 9 000 ₽ в месяц, наберется за 20 месяцев. Отпуск на 90 000 ₽ получает оставшиеся 6 000 ₽ в месяц и будет готов через 15 месяцев.","Если в этом месяце пришлось потратить больше, план сдвигает дату, а не ломается. Видно, на сколько отложится отпуск и что можно сделать, чтобы успеть."]),
  ("Шаги: как начать копить в Кубыше",["Укажите даты и суммы зарплаты и аванса.","Добавьте обязательные платежи: аренду, кредиты, подписки.","Создайте цели с суммой и сроком, Кубыш посчитает взнос в месяц и дату.","С каждой получки откладывайте сумму, которую предлагает план.","Перед крупной покупкой проверьте, как она сдвинет цели."]),
  ("Где хранить накопленное",["Деньги на цели удобнее держать отдельно от карты для трат: на накопительном счете или вкладе, срок которого совпадает со сроком цели. Кубыш подбирает вклады и накопительные счета под сроки ваших целей и показывает, сколько они принесут в месяц. Счет он не открывает и деньги не переводит, это решение остается за вами."]),
  ("Кому подойдет Кубыш",["Тем, кто получает зарплату, с авансом и премиями или без них, и пользуется iPhone. При нерегулярном доходе план будет неточным, версии для Android пока нет."])],
 "faq":[("Есть ли бесплатное приложение-копилка?","В Кубыше первый период до получки бесплатный. Дальше подписка, цена указана на странице приложения в App Store."),
        ("Можно ли копить на несколько целей сразу?","Да. Цели идут по приоритету: сначала самая важная, потом следующая. Для каждой видна сумма в месяц и дата."),
        ("Нужно ли подключать банк?","Нет. Достаточно указать зарплату, обязательные платежи и цели. Траты можно вносить скриншотом из банковского приложения."),
        ("Чем Кубыш отличается от копилки в банке?","Банковская копилка откладывает деньги по правилу. Кубыш планирует: считает, сколько откладывать с каждой зарплаты, и показывает, когда вы дойдете до каждой цели. Их можно использовать вместе."),
        ("Где хранятся деньги?","В вашем банке. Кубыш не хранит и не переводит деньги, он держит план и подбирает вклады под сроки целей.")],
 "related":["kalkulyator-nakopleniy","finansovye-celi","finansovaya-podushka"]}


PAGES["tablica-dohodov-i-rashodov"] = {
 "published":"2026-10-05", "modified":"2026-10-05",
 "title":"Таблица доходов и расходов: скачать шаблон Excel для личного бюджета",
 "desc":"Шаблон таблицы доходов и расходов на месяц: доходы, обязательные платежи, цели и бюджет на день. Excel и Google Таблицы, пример на зарплату 80 000 ₽.",
 "h1":"Таблица доходов и расходов: шаблон для личного бюджета от получки до получки",
 "lead":"Таблица доходов и расходов полезна, только если отвечает на вопрос «сколько можно тратить сегодня». Ниже готовый шаблон Excel, пример заполнения и правила, которые не дают бросить таблицу через месяц.",
 "answer":"Ведите таблицу от получки до получки, а не по календарю. Доходы минус обязательные платежи минус взносы на цели дают деньги на жизнь. Деньги на жизнь, деленные на дни до следующей зарплаты, дают бюджет на день. Траты записывайте каждый день и сравнивайте с этим бюджетом.",
 "tool":"budget-template",
 "app":{"title":"Не хотите заполнять руками?","img":"screenshot-1-7.webp","alt":"Внесение трат скриншотом из банка в Кубыше",
        "points":["Траты одним скриншотом из любого банка, категории расставляются сами","Бюджет на день и запас в днях до получки пересчитываются после каждой траты","Цели с суммой в месяц и датой, как в шаблоне, только без формул","Утром и вечером короткий план в уведомлении"]},
 "sections":[
  ("Из чего состоит таблица доходов и расходов",[
   "Хорошая таблица отвечает не на вопрос «куда ушли деньги», а на вопрос «сколько еще можно потратить». Для этого в ней пять блоков, и порядок важен.",
   "Доходы за период. Аванс, зарплата, премия, подработка. Каждый доход с датой: если зарплата приходит дважды в месяц, это два разных поступления, и деньги между ними нужно растянуть до следующего.",
   "Обязательные платежи. Аренда или ипотека, кредиты, связь, подписки, проездной. Это деньги, которые уйдут в любом случае, поэтому их вычитают первыми, до любых трат.",
   "Цели. Подушка безопасности, отпуск, крупная покупка. Сумму на цели откладывают в день получки. Если откладывать «что останется в конце месяца», обычно не остается ничего.",
   "Деньги на жизнь и бюджет на день. Это главная строка таблицы: доходы минус обязательные минус цели, деленные на число дней до следующей зарплаты.",
   "Траты по факту. Дата, категория, сумма. Их сравнивают с бюджетом на день, а раз в период смотрят, какие категории съели больше всего."]),
  ("Пример: зарплата 80 000 ₽ с авансом",[
   "Так выглядит заполненный шаблон для человека, который получает аванс 10-го и зарплату 25-го числа.",
   '<table class="data"><tr><th>Строка</th><th>Сумма</th></tr><tr><td>Аванс 10-го</td><td>32 000 ₽</td></tr><tr><td>Зарплата 25-го</td><td>48 000 ₽</td></tr><tr class="total"><td>Доходы за месяц</td><td>80 000 ₽</td></tr><tr><td>Аренда</td><td>25 000 ₽</td></tr><tr><td>Кредит</td><td>6 000 ₽</td></tr><tr><td>Связь, подписки, проездной</td><td>4 000 ₽</td></tr><tr class="total"><td>Обязательные платежи</td><td>35 000 ₽</td></tr><tr><td>Подушка безопасности</td><td>9 000 ₽</td></tr><tr><td>Отпуск</td><td>6 000 ₽</td></tr><tr class="total"><td>Отложить на цели</td><td>15 000 ₽</td></tr><tr class="total"><td>Деньги на жизнь</td><td>30 000 ₽</td></tr><tr class="total"><td>Бюджет на день (30 дней)</td><td>1 000 ₽</td></tr></table>',
   "Получается 1 000 ₽ в день на еду, кафе, такси, покупки и развлечения. Если в понедельник потрачено 2 500 ₽, бюджет на оставшиеся дни уменьшается, и это видно сразу, а не в конце месяца.",
   "Обратите внимание: цели стоят в таблице раньше трат. Это и есть главный прием. Сначала заплатить себе, потом жить на остаток."]),
  ("Шаги: как заполнить таблицу за 15 минут",[
   "Скачайте шаблон и откройте лист «Бюджет периода».",
   "Впишите доходы за месяц или за период до следующей получки с датами.",
   "Перечислите обязательные платежи. Возьмите выписку за прошлый месяц, чтобы ничего не забыть: подписки любят прятаться.",
   "Решите, сколько откладывать на цели. Начните с подушки безопасности, хотя бы 5–10% дохода.",
   "Укажите число дней до следующей получки. Таблица посчитает бюджет на день.",
   "Каждый вечер записывайте траты на листе «Траты». Остаток и доли по категориям посчитаются сами."]),
  ("Почему таблицу бросают через месяц",[
   "Самая частая причина: ручной ввод. Каждая покупка требует открыть файл, найти строку и вписать сумму. Через 2–3 недели пропущенные дни копятся, таблица перестает совпадать с реальностью, и ее закрывают.",
   "Вторая причина: таблица считает прошлое. Если в ней нет строки «бюджет на день», она показывает, куда ушли деньги, но не помогает решить, можно ли купить что-то сегодня.",
   "Третья причина: календарный месяц. Зарплата приходит 25-го, а таблица считает с 1-го. В итоге в начале месяца денег якобы много, а к 20-му числу внезапно мало.",
   "Шаблон выше решает вторую и третью проблему. Первую решает только автоматизация: например, приложение, куда траты вносятся скриншотом из банка."]),
  ("Excel, Google Таблицы или приложение",[
   "Excel и Numbers удобны на компьютере и позволяют настроить что угодно. Минус: на телефоне вносить траты неудобно, а тратим мы чаще с телефона.",
   "Google Таблицы открываются с любого устройства и синхронизируются. Шаблон загружается через Файл → Импорт. Минус тот же: ввод трат с телефона медленный.",
   "Приложение для бюджета берет на себя ввод и пересчет. Кубыш строит тот же план, что в шаблоне, только сам: доходы по датам получки, обязательные платежи, цели с датами и бюджет на день. Траты вносятся скриншотом из банка, подключать банк не нужно.",
   "Начать можно с таблицы. Если через 2 недели вы все еще заполняете ее каждый день, отлично. Если нет, это сигнал перейти на приложение, а не винить себя."]),
  ("Как читать итоги периода",[
   "В конце периода посмотрите на три цифры. Отложили ли вы на цели всю запланированную сумму. Уложились ли в деньги на жизнь. Какие 2–3 категории заняли больше всего.",
   "Ищите один крупный рычаг, а не десять мелких запретов. Обычно это доставка еды, такси или подписки. Сократить одну такую категорию на треть проще, чем следить за каждой покупкой.",
   "Если денег на жизнь регулярно не хватает, проблема скорее в обязательных платежах или в слишком большой сумме на цели. Пересоберите план, а не урезайте еду."])],
 "faq":[
  ("Как вести таблицу доходов и расходов?","Раз в период заполните доходы, обязательные платежи и цели, а траты записывайте каждый день. Главная строка — бюджет на день: деньги на жизнь, деленные на дни до следующей зарплаты."),
  ("Как сделать таблицу доходов и расходов в Excel?","Проще всего скачать готовый шаблон выше: в нем настроены формулы итогов, бюджета на день и трат по категориям. Если делаете сами, начните с пяти блоков: доходы, обязательные, цели, деньги на жизнь, траты."),
  ("Есть ли шаблон для Google Таблиц?","Да, тот же файл. Откройте sheets.google.com, выберите Файл → Импорт → Загрузка и загрузите скачанный шаблон. Формулы сохранятся."),
  ("Вести таблицу за месяц или от зарплаты до зарплаты?","От зарплаты до зарплаты. Так бюджет на день совпадает с реальными деньгами на карте, а не с календарем."),
  ("Какие категории расходов выбрать?","Начните с 6–9: продукты, кафе и доставка, транспорт, дом, здоровье, одежда, развлечения, подарки, другое. Дробить сильнее имеет смысл, только если категория занимает больше 20% трат."),
  ("Сколько откладывать на цели?","Начните с 5–10% дохода на подушку безопасности, пока она не достигнет 3–6 месячных обязательных расходов. Потом добавляйте другие цели по приоритету."),
  ("Чем приложение лучше таблицы?","Приложение берет на себя ввод трат и пересчет. В Кубыше траты вносятся скриншотом из банка, а бюджет на день и прогноз по целям обновляются сами.")],
 "related":["byudzhet-na-mesyats","kak-raspredelit-zarplatu","prilozhenie-dlya-kontrolya-rashodov"]}


def app_html(app: dict | None) -> str:
    if not app:
        return ""
    points = "".join(f"<li>{html.escape(x)}</li>" for x in app["points"])
    return (f'<section class="app" aria-label="Кубыш"><img src="/img/{app["img"]}" width="852" height="1791" alt="{html.escape(app["alt"])}" loading="lazy" decoding="async">'
            f'<div><h2>{html.escape(app["title"])}</h2><ul>{points}</ul><a class="btn js-appstore" href="{APP_STORE}">Скачать в App Store</a>'
            f'<p class="note">Первый период до получки бесплатно · iPhone · без подключения банка</p></div></section>')


def tool_html(kind: str | None) -> str:
    if kind == "budget-template":
        return ('<section class="download" aria-label="Скачать шаблон"><h2>Скачать таблицу доходов и расходов</h2>'
                '<p>Excel-файл на период от получки до получки: доходы, обязательные платежи, цели, бюджет на день и траты по категориям. Формулы уже настроены, пример заполнен.</p>'
                '<a class="btn js-download" href="/files/tablica-dohodov-i-rashodov-kubysh.xlsx" download>Скачать Excel (.xlsx)</a>'
                '<p class="note">Для Google Таблиц: sheets.google.com → Файл → Импорт → Загрузка. Открывается и в Numbers на Mac и iPhone.</p></section>')
    if kind == "savings":
        return '''<section class="tool" aria-label="Калькулятор накоплений"><h2>Посчитать взнос</h2><label for="target">Цель, ₽</label><input id="target" inputmode="numeric" value="500000"><label for="start">Уже накоплено, ₽</label><input id="start" inputmode="numeric" value="50000"><label for="months">Срок, месяцев</label><input id="months" inputmode="numeric" value="18"><output id="savings-output"></output><p class="note">Без учёта процентов, инфляции и инвестиционной доходности.</p></section>'''
    if kind == "cushion":
        return '''<section class="tool" aria-label="Калькулятор финансовой подушки"><h2>Посчитать резерв</h2><label for="essential">Обязательные расходы в месяц, ₽</label><input id="essential" inputmode="numeric" value="60000"><label for="cushion-months">Сколько месяцев покрыть</label><input id="cushion-months" inputmode="numeric" value="3"><output id="cushion-output"></output><p class="note">Это ориентир по введённым расходам, а не индивидуальная финансовая рекомендация.</p></section>'''
    return ""


def page(slug: str, cfg: dict) -> str:
    canonical = f"https://kubysh.com/{slug}/"
    related = []
    for rel in cfg.get("related", []):
        if rel in PAGES:
            name = PAGES[rel]["h1"]
        elif rel == "finansovaya-podushka": name = "Финансовая подушка безопасности"
        elif rel == "skolko-mozhno-tratit": name = "Сколько можно тратить до зарплаты"
        else: name = rel.replace('-', ' ').capitalize()
        related.append(f'<a class="card" href="/{rel}/"><strong>{html.escape(name)}</strong><span>Продолжить по теме →</span></a>')
    sections = []
    for heading, paras in cfg["sections"]:
        sections.append(f"<h2>{html.escape(heading)}</h2>")
        if heading.lower().startswith("простая система") or heading.lower().startswith("шаг"):
            sections.append("<ol class=\"steps\">"+"".join(f"<li>{html.escape(p)}</li>" for p in paras)+"</ol>")
        else:
            sections.extend(p if p.startswith("<") else f"<p>{html.escape(p)}</p>" for p in paras)
    faq_html = "".join(f'<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>' for q,a in cfg["faq"])
    faq_schema = [{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in cfg["faq"]]
    schema = {"@context":"https://schema.org","@graph":[
        {"@type":"Organization","@id":"https://kubysh.com/#org","name":SITE_NAME,"url":SITE_URL,"logo":{"@type":"ImageObject","url":"https://kubysh.com/icon-192.png","width":192,"height":192}},
        {"@type":"WebSite","@id":"https://kubysh.com/#website","url":SITE_URL,"name":"Кубыш — финансовый навигатор","inLanguage":"ru-RU","publisher":{"@id":"https://kubysh.com/#org"}},
        {"@type":"BreadcrumbList","@id":f"{canonical}#breadcrumbs","itemListElement":[{"@type":"ListItem","position":1,"name":"Кубыш","item":SITE_URL},{"@type":"ListItem","position":2,"name":"Личные финансы","item":"https://kubysh.com/lichnye-finansy/"},{"@type":"ListItem","position":3,"name":cfg["h1"],"item":canonical}]},
        {"@type":"Article","@id":f"{canonical}#article","headline":cfg["h1"],"description":cfg["desc"],"image":SOCIAL_IMAGE,"inLanguage":"ru-RU","datePublished":cfg.get("published",PUBLISHED_DATE),"dateModified":cfg.get("modified",MODIFIED_DATE),"author":{"@type":"Organization","name":"Команда Кубыш","url":"https://kubysh.com/metodologiya/"},"publisher":{"@id":"https://kubysh.com/#org"},"isPartOf":{"@id":"https://kubysh.com/#website"},"mainEntityOfPage":canonical,"citation":[url for _,url in SOURCES]},
        {"@type":"FAQPage","@id":f"{canonical}#faq","mainEntity":faq_schema}
    ]}
    return f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(cfg['title'])}</title><meta name="description" content="{html.escape(cfg['desc'])}"><meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large"><link rel="canonical" href="{canonical}"><meta property="og:type" content="article"><meta property="og:locale" content="ru_RU"><meta property="og:site_name" content="Кубыш"><meta property="og:url" content="{canonical}"><meta property="og:title" content="{html.escape(cfg['title'])}"><meta property="og:description" content="{html.escape(cfg['desc'])}"><meta property="og:image" content="{SOCIAL_IMAGE}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="Кубыш — финансовый навигатор до получки"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{html.escape(cfg['title'])}"><meta name="twitter:description" content="{html.escape(cfg['desc'])}"><meta name="twitter:image" content="{SOCIAL_IMAGE}"><link rel="stylesheet" href="/assets/seo.css?v={SEO_ASSET_VERSION}"><script defer src="/assets/seo.js?v={SEO_JS_VERSION}"></script><script type="application/ld+json">{json.dumps(schema,ensure_ascii=False)}</script></head><body><header><div class="wrap top"><a class="logo" href="/">Кубы<span>ш</span></a><nav class="topnav"><a class="hub" href="/lichnye-finansy/">Личные финансы</a><a class="install js-appstore" href="{APP_STORE}">Установить</a></nav></div></header><main class="wrap"><nav class="crumbs"><a href="/">Кубыш</a> → <a href="/lichnye-finansy/">Личные финансы</a> → {html.escape(cfg['h1'])}</nav><h1>{html.escape(cfg['h1'])}</h1><p class="lead">{html.escape(cfg['lead'])}</p><div class="answer"><strong>Коротко:</strong> {html.escape(cfg['answer'])}</div>{app_html(cfg.get('app'))}{tool_html(cfg.get('tool'))}{''.join(sections)}<section class="faq"><h2>Частые вопросы</h2>{faq_html}</section><section class="related"><h2>Что читать дальше</h2><div class="grid">{''.join(related)}</div></section><section><h2>Источники и методика</h2><p>Материал подготовлен редакцией Кубыша как образовательный. Мы отделяем общую арифметику бюджета от индивидуальных финансовых решений и не подменяем персональную консультацию.</p><ul class="sources">{''.join(f'<li><a href="{u}" rel="noopener">{html.escape(n)}</a></li>' for n,u in SOURCES)}<li><a href="/metodologiya/">Как мы готовим материалы и расчёты</a></li></ul></section><div class="cta"><h2>Пусть план пересчитывается сам</h2><p>Кубыш показывает, сколько можно потратить сегодня до следующего дохода с учётом обязательных платежей и целей.</p><a class="btn js-appstore" href="{APP_STORE}">Открыть в App Store</a></div><p class="updated">Обновлено {cfg.get('modified',MODIFIED_DATE)}. Не является индивидуальной финансовой рекомендацией.</p></main><footer><div class="wrap"><div class="links"><a href="/lichnye-finansy/">Все гайды</a><a href="/o-proekte/">О проекте</a><a href="/metodologiya/">Методология</a><a href="/privacy/">Политика ПД</a><a href="/terms/">Соглашение</a></div>© Кубыш</div></footer></body></html>'''


def hub() -> str:
    cards = "".join(f'<a class="card" href="/{s}/"><strong>{html.escape(c["h1"])}</strong><span>{html.escape(c["desc"])}</span></a>' for s,c in PAGES.items())
    canonical = "https://kubysh.com/lichnye-finansy/"
    title = "Материалы Кубыша: личные финансы, история и методология"
    desc = "История Кубыша и Кирилла Попова, методология расчётов, гайды и калькуляторы по бюджету, расходам, накоплениям, подушке и финансовым целям."
    schema={"@context":"https://schema.org","@graph":[
        {"@type":"Organization","@id":"https://kubysh.com/#org","name":SITE_NAME,"url":SITE_URL},
        {"@type":"WebSite","@id":"https://kubysh.com/#website","url":SITE_URL,"name":"Кубыш — финансовый навигатор","inLanguage":"ru-RU","publisher":{"@id":"https://kubysh.com/#org"}},
        {"@type":"CollectionPage","@id":f"{canonical}#page","name":"Материалы Кубыша","url":canonical,"description":desc,"inLanguage":"ru-RU","dateModified":HUB_MODIFIED_DATE,"isPartOf":{"@id":"https://kubysh.com/#website"},"about":["Кубыш","Кирилл Попов","личные финансы","бюджет","расходы","накопления"],"hasPart":[{"@id":"https://kubysh.com/o-proekte/#page"},{"@id":"https://kubysh.com/metodologiya/#page"}]+[{"@id":f"https://kubysh.com/{slug}/#article"} for slug in PAGES]},
        {"@type":"BreadcrumbList","@id":f"{canonical}#breadcrumbs","itemListElement":[{"@type":"ListItem","position":1,"name":"Кубыш","item":SITE_URL},{"@type":"ListItem","position":2,"name":"Материалы","item":canonical}]}
    ]}
    social = f'''<meta property="og:type" content="website"><meta property="og:locale" content="ru_RU"><meta property="og:site_name" content="Кубыш"><meta property="og:url" content="{canonical}"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:image" content="{SOCIAL_IMAGE}"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{title}"><meta name="twitter:description" content="{desc}"><meta name="twitter:image" content="{SOCIAL_IMAGE}">'''
    return f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><meta name="description" content="{desc}"><meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large"><link rel="canonical" href="{canonical}">{social}<link rel="stylesheet" href="/assets/seo.css?v={SEO_ASSET_VERSION}"><script defer src="/assets/seo.js?v={SEO_JS_VERSION}"></script><script type="application/ld+json">{json.dumps(schema,ensure_ascii=False)}</script></head><body><header><div class="wrap top"><a class="logo" href="/">Кубы<span>ш</span></a><nav class="topnav"><a class="hub" href="/o-proekte/">О проекте</a><a class="install js-appstore" href="{APP_STORE}">Установить</a></nav></div></header><main class="wrap"><nav class="crumbs"><a href="/">Кубыш</a> → Личные финансы</nav><h1>Личные финансы без магических процентов</h1><p class="lead">Здесь собраны практические материалы для разных финансовых задач: понять, куда уходят деньги, спланировать бюджет до следующего дохода, начать копить и подготовиться к крупной покупке.</p><div class="answer"><strong>С чего начать:</strong> если деньги заканчиваются раньше следующего дохода — начните с контроля финансов и бюджета. Если бюджет стабилен — переходите к накоплениям и целям.</div><h2>Гайды и инструменты</h2><div class="grid">{cards}</div><h2>Уже опубликовано</h2><div class="grid"><a class="card" href="/skolko-mozhno-tratit/"><strong>Сколько можно тратить в день</strong><span>Расчёт свободной суммы до зарплаты</span></a><a class="card" href="/finansovaya-podushka/"><strong>Финансовая подушка безопасности</strong><span>Как считать резерв по необходимым расходам</span></a><a class="card" href="/alternativa-dzen-mani/"><strong>Альтернатива Дзен-мани</strong><span>Другой подход к контролю денег</span></a></div><div class="cta"><h2>От гайда к своему плану</h2><p>Кубыш связывает обязательные платежи, цели и фактические траты в один план до следующего дохода.</p><a class="btn js-appstore" href="{APP_STORE}">Открыть в App Store</a></div><p class="updated">Обновлено {MODIFIED_DATE}. Материалы образовательные и не являются индивидуальной финансовой рекомендацией.</p></main><footer><div class="wrap"><div class="links"><a href="/o-proekte/">О проекте</a><a href="/metodologiya/">Методология</a><a href="/privacy/">Политика ПД</a><a href="/terms/">Соглашение</a></div>© Кубыш</div></footer></body></html>'''


def methodology() -> str:
    canonical = "https://kubysh.com/metodologiya/"
    title = "Методология финансовых материалов — Кубыш"
    desc = "Как команда Кубыша готовит материалы о личных финансах: источники, расчёты, обновления, границы образовательного контента."
    schema={"@context":"https://schema.org","@graph":[
        {"@type":"Organization","@id":"https://kubysh.com/#org","name":SITE_NAME,"url":SITE_URL},
        {"@type":"AboutPage","@id":f"{canonical}#page","url":canonical,"name":title,"description":desc,"inLanguage":"ru-RU","dateModified":MODIFIED_DATE,"about":{"@id":"https://kubysh.com/#org"},"citation":[url for _,url in SOURCES]},
        {"@type":"BreadcrumbList","@id":f"{canonical}#breadcrumbs","itemListElement":[{"@type":"ListItem","position":1,"name":"Кубыш","item":SITE_URL},{"@type":"ListItem","position":2,"name":"Методология","item":canonical}]}
    ]}
    return f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><meta name="description" content="{desc}"><meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large"><link rel="canonical" href="{canonical}"><meta property="og:type" content="website"><meta property="og:locale" content="ru_RU"><meta property="og:site_name" content="Кубыш"><meta property="og:url" content="{canonical}"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:image" content="{SOCIAL_IMAGE}"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{SOCIAL_IMAGE}"><link rel="stylesheet" href="/assets/seo.css?v={SEO_ASSET_VERSION}"><script defer src="/assets/seo.js?v={SEO_JS_VERSION}"></script><script type="application/ld+json">{json.dumps(schema,ensure_ascii=False)}</script></head><body><header><div class="wrap top"><a class="logo" href="/">Кубы<span>ш</span></a><nav class="topnav"><a class="hub" href="/lichnye-finansy/">Личные финансы</a><a class="install js-appstore" href="{APP_STORE}">Установить</a></nav></div></header><main class="wrap"><nav class="crumbs"><a href="/">Кубыш</a> → Методология</nav><h1>Как мы готовим материалы о личных финансах</h1><p class="lead">Финансы относятся к темам, где красивый совет может дорого стоить. Поэтому мы отделяем проверяемую арифметику и общую финансовую грамотность от персональных решений.</p><h2>Принципы</h2><ol><li><strong>Пишем под задачу человека.</strong> Разные поисковые интенты получают отдельные материалы, но мы не создаём страницы только ради перестановки ключевых слов.</li><li><strong>Показываем формулу.</strong> Если есть расчёт, из текста должно быть понятно, из каких чисел он получился.</li><li><strong>Не обещаем доходность.</strong> Калькуляторы накоплений по умолчанию считают собственные взносы без выдуманной инвестиционной доходности.</li><li><strong>Ссылаемся на первичные и профильные источники.</strong> Для общей финансовой грамотности используем в том числе материалы Банка России и проекта «Финансовая культура».</li><li><strong>Обновляем при изменении продукта или правил.</strong> На материалах стоит дата обновления.</li></ol><h2>Граница материала</h2><p>Статьи и калькуляторы на kubysh.com — образовательный контент. Они не учитывают все обстоятельства конкретного человека и не являются индивидуальной инвестиционной, кредитной, налоговой или юридической рекомендацией.</p><h2>О продукте</h2><p>Кубыш — приложение для планирования денег между доходами: оно учитывает обязательные платежи, цели и фактические траты и пересчитывает доступную сумму после изменений. Для базового сценария не требуется доступ к банковскому счёту.</p><h2>Источники</h2><ul class="sources">{''.join(f'<li><a href="{u}" rel="noopener">{html.escape(n)}</a></li>' for n,u in SOURCES)}</ul><p class="updated">Последнее обновление: {MODIFIED_DATE}</p></main><footer><div class="wrap"><div class="links"><a href="/lichnye-finansy/">Все гайды</a><a href="/o-proekte/">О проекте</a><a href="/privacy/">Политика ПД</a><a href="/terms/">Соглашение</a></div>© Кубыш</div></footer></body></html>'''


def about() -> str:
    canonical = "https://kubysh.com/o-proekte/"
    title = "Кирилл Попов и история приложения Кубыш"
    desc = "Как Кирилл Попов создал Кубыш: от личного вопроса о деньгах до iOS-приложения, которое показывает, сколько можно потратить сегодня до получки."
    person_id = f"{canonical}#kirill-popov"
    articles = [
        {
            "platform": "Хабр",
            "title": "Я попросил ИИ самостоятельно опубликовать мое приложение в App Store и ушел сочинять лампу",
            "url": "https://habr.com/ru/articles/1067120/",
        },
        {
            "platform": "Хабр",
            "title": "Месяц Кубыша в App Store: 4 тысячи показов, 155 установок и 52 товарища из Шанхая",
            "url": "https://habr.com/ru/articles/1078768/",
        },
        {
            "platform": "vc.ru",
            "title": "Собрал приложение с ИИ за 4 чел-месяца. Посчитал, сколько это стоило бы командой",
            "url": "https://vc.ru/id6066630/3140281-kak-ii-snizhaet-stoimost-razrabotki-prilozheniy-dlya-biznesa",
        },
    ]
    schema = {"@context": "https://schema.org", "@graph": [
        {"@type": "Person", "@id": person_id, "name": "Кирилл Попов", "url": canonical,
         "image": {"@type": "ImageObject", "url": ABOUT_IMAGE, "width": 746, "height": 810},
         "jobTitle": "Создатель приложения «Кубыш»",
         "description": "Product Lead с семилетним опытом в цифровых продуктах и создатель приложения для личных финансов «Кубыш».",
         "sameAs": ["https://habr.com/ru/users/popov_kirill_a/", "https://vc.ru/id6066630"],
         "subjectOf": [{"@type": "Article", "headline": item["title"], "url": item["url"]} for item in articles]},
        {"@type": "Organization", "@id": "https://kubysh.com/#org", "name": SITE_NAME, "url": SITE_URL,
         "founder": {"@id": person_id}},
        {"@type": "WebSite", "@id": "https://kubysh.com/#website", "url": SITE_URL,
         "name": "Кубыш", "inLanguage": "ru-RU", "publisher": {"@id": "https://kubysh.com/#org"}},
        {"@type": "SoftwareApplication", "@id": "https://kubysh.com/#app", "name": SITE_NAME,
         "applicationCategory": "FinanceApplication", "operatingSystem": "iOS 17.6+", "url": SITE_URL,
         "downloadUrl": APP_STORE, "creator": {"@id": person_id}},
        {"@type": "AboutPage", "@id": f"{canonical}#page", "url": canonical, "name": title,
         "description": desc, "inLanguage": "ru-RU", "dateModified": MODIFIED_DATE,
         "mainEntity": {"@id": person_id}, "isPartOf": {"@id": "https://kubysh.com/#website"}},
        {"@type": "BreadcrumbList", "@id": f"{canonical}#breadcrumbs", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Кубыш", "item": SITE_URL},
            {"@type": "ListItem", "position": 2, "name": "О проекте", "item": canonical},
        ]},
    ]}
    article_cards = "".join(
        f'<a class="about-article" href="{item["url"]}" target="_blank" rel="noopener noreferrer"><small>{item["platform"]}</small><strong>{item["title"]}</strong><span>Читать на площадке</span></a>'
        for item in articles
    )
    return f'''<!doctype html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}"><meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large"><link rel="canonical" href="{canonical}">
<meta property="og:type" content="profile"><meta property="og:locale" content="ru_RU"><meta property="og:site_name" content="Кубыш"><meta property="og:url" content="{canonical}"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:image" content="{SOCIAL_IMAGE}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="Кубыш — финансовый навигатор до получки"><meta property="profile:first_name" content="Кирилл"><meta property="profile:last_name" content="Попов">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{title}"><meta name="twitter:description" content="{desc}"><meta name="twitter:image" content="{SOCIAL_IMAGE}">
<link rel="stylesheet" href="/assets/seo.css?v={SEO_ASSET_VERSION}"><link rel="stylesheet" href="/assets/about.css?v=20260918c"><script defer src="/assets/seo.js?v={SEO_JS_VERSION}"></script><script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script></head>
<body><header><div class="about-wrap top"><a class="logo" href="/">Кубы<span>ш</span></a><nav class="topnav" aria-label="Основная навигация"><a class="hub" href="/lichnye-finansy/">Личные финансы</a><a class="install js-appstore" href="{APP_STORE}">Установить</a></nav></div></header>
<main class="about-main">
<section class="about-wrap about-hero"><div class="about-hero-copy"><p class="about-kicker">О проекте</p><p class="about-name">Кирилл Попов</p><h1>От личного вопроса <span>к Кубышу</span></h1><p class="about-lead">Кубыш начался с простого вопроса: сколько можно потратить сегодня, чтобы денег хватило до получки и важные планы не сдвинулись.</p><p class="about-role"><strong>Создатель Кубыша</strong><span>Product Lead</span><span>7 лет в цифровых продуктах</span></p></div><figure class="about-photo-wrap"><img class="about-photo" src="/img/kirill-popov.jpg" width="746" height="810" alt="Кирилл Попов с кошкой Фичей" fetchpriority="high"><figcaption class="about-caption"><span>Кирилл Попов, создатель Кубыша</span><span>Фича, специалист по связям с общественностью</span></figcaption></figure></section>
<section class="about-wrap about-section"><div class="about-copy"><p class="about-section-label">Личный мотив</p><h2>Почему появился Кубыш</h2><p>У Кирилла было несколько целей и обычная жизнь между ними: обязательные платежи, покупки, отпуск и траты, которые невозможно держать в голове одновременно. Готовые инструменты помогали посмотреть назад или копить на одну цель, но не отвечали, какое финансовое действие безопасно прямо сейчас.</p><p>В декабре 2025 года Кирилл начал собирать собственный инструмент. Он не был мобильным разработчиком, зато семь лет строил цифровые продукты и умел превращать задачу человека в работающий сценарий.</p><div class="about-quote">Не еще один отчет о прошлом, а спокойный ответ на вопрос: сколько можно потратить сегодня</div></div></section>
<section class="about-wrap about-section"><p class="about-section-label">Доверие к расчету</p><h2>Три принципа продукта</h2><div class="about-principles"><article class="about-principle"><span class="about-principle-mark" aria-hidden="true">01</span><b>Сначала спокойствие</b><p>Кубыш показывает доступную сумму на сегодня и хватит ли денег до следующей получки.</p></article><article class="about-principle"><span class="about-principle-mark" aria-hidden="true">02</span><b>Деньги считает устройство</b><p>Финансовая модель работает на устройстве и не передает расчеты языковой модели.</p></article><article class="about-principle"><span class="about-principle-mark" aria-hidden="true">03</span><b>ИИ не считает деньги</b><p>Он объясняет готовый расчет человеческим языком, но не участвует в финансовой математике.</p></article></div></section>
<section class="about-wrap about-section"><p class="about-section-label">Путь продукта</p><h2>Как идея стала приложением</h2><div class="about-timeline"><article class="about-step"><strong>Декабрь 2025</strong><span>Начался личный эксперимент: можно ли собрать финансовый навигатор без опыта мобильной разработки.</span></article><article class="about-step"><strong>9 июля 2026</strong><span>Первая версия Кубыша появилась в App Store после семи месяцев разработки и проверки гипотез.</span></article><article class="about-step"><strong>Сейчас</strong><span>Кубыш развивается вокруг реальных сценариев: получки, обязательных платежей, ежедневных трат и целей.</span></article></div></section>
<section class="about-wrap about-section"><div class="about-copy"><p class="about-section-label">Публикации автора</p><h2>История от первого лица</h2><p>Кирилл открыто пишет о создании Кубыша, работе с ИИ, запуске в App Store и продуктовых ошибках. Это не пересказ со стороны, а дневник разработки с конкретными решениями и цифрами.</p></div><div class="about-articles">{article_cards}</div></section>
<section class="about-wrap"><div class="about-cta"><div><h2>Посмотреть, как работает Кубыш</h2><p>Финансовый навигатор до следующей получки для iPhone.</p></div><a class="btn js-appstore" href="{APP_STORE}">Открыть в App Store</a></div></section>
</main><footer><div class="about-footer"><div class="links"><a href="/">Главная</a><a href="/lichnye-finansy/">Гайды</a><a href="/metodologiya/">Методология</a><a href="/privacy/">Политика ПД</a><a href="/terms/">Соглашение</a></div>© Кубыш</div></footer></body></html>'''


def sitemap() -> str:
    urls = ["", "lichnye-finansy", *PAGES.keys(), "metodologiya", "o-proekte", "skolko-mozhno-tratit", "finansovaya-podushka", "alternativa-dzen-mani", "privacy", "terms"]
    unique=[]
    for u in urls:
        if u not in unique: unique.append(u)
    rows=[]
    for slug in unique:
        loc="https://kubysh.com/" + (f"{slug}/" if slug else "")
        lastmod = PAGES[slug].get("modified", MODIFIED_DATE) if slug in PAGES and "modified" in PAGES[slug] else MAIN_MODIFIED_DATE if slug == "" else HUB_MODIFIED_DATE if slug == "lichnye-finansy" else MODIFIED_DATE if slug in PAGES or slug in (
            "metodologiya", "o-proekte", "skolko-mozhno-tratit",
            "finansovaya-podushka", "alternativa-dzen-mani",
        ) else "2026-09-16"
        rows.append(f"  <url><loc>{loc}</loc><lastmod>{lastmod}</lastmod></url>")
    return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+"\n".join(rows)+'\n</urlset>\n'


def llms() -> str:
    return """# Кубыш

> Кубыш — финансовый навигатор для iPhone: приложение строит личный бюджет от одной получки до следующей. Каждый день оно показывает, сколько можно потратить сегодня, на сколько дней хватит денег до зарплаты и успевает ли человек к своим целям.

## Для кого
- Люди со стабильной зарплатой (раз или два в месяц, с авансом и премиями или без них) и iPhone.
- При нерегулярном доходе (фриланс, бизнес) прогноз будет неточным. Версии для Android нет.

## Проверяемые факты о продукте
- Платформа: iOS 17.6 и новее. Язык: русский.
- App Store: https://apps.apple.com/app/id6778792103
- «Получка» показывает бюджет на день, запас в днях до следующей получки и темп периода (дефицит или профицит к концу периода).
- Обязательные платежи, плановые траты и взносы в цели вычитаются до расчета бюджета на день.
- Траты вносятся скриншотом из любого банковского приложения или вручную. Подключать банк не нужно, логины и пароли от банка приложению не нужны.
- После каждой траты пересчитываются бюджет на завтра и прогноз по целям.
- Накопления лежат на одном счете, внутри приложение распределяет их по целям и подушке и показывает актуальные даты достижения.
- Утром и вечером приходят уведомления с планом и напоминанием внести траты.
- Финансовая математика выполняется на устройстве; языковая модель только объясняет рассчитанный результат.
- Цена: первый период до получки бесплатный, дальше подписка; актуальная цена указана в App Store.
- Кубыш не является инвестиционным советником, не перемещает деньги пользователя и не выдает кредиты.

## Чем отличается от Дзен-мани и CoinKeeper
Учетные приложения показывают, куда ушли деньги. Кубыш планирует вперед: отвечает до покупки, сколько можно потратить сегодня, чтобы хватило до зарплаты и на цели. Подробно: https://kubysh.com/alternativa-dzen-mani/

## Основные страницы
- https://kubysh.com/ — официальная страница приложения и ссылка на App Store
- https://kubysh.com/skolko-mozhno-tratit/ — формула доступной суммы до зарплаты
- https://kubysh.com/kak-raspredelit-zarplatu/ — как распределить зарплату
- https://kubysh.com/byudzhet-na-mesyats/ — бюджет на месяц
- https://kubysh.com/prilozhenie-dlya-kontrolya-rashodov/ — как выбрать приложение для контроля расходов
- https://kubysh.com/lichnye-finansy/ — все гайды и калькуляторы
- https://kubysh.com/finansovaya-podushka/ — финансовая подушка
- https://kubysh.com/tablica-dohodov-i-rashodov/ — таблица доходов и расходов: шаблон Excel и пример
- https://kubysh.com/prilozhenie-kopilka/ — приложение-копилка для iPhone: цели, сумма в месяц, дата
- https://kubysh.com/kalkulyator-nakopleniy/ — калькулятор накоплений
- https://kubysh.com/kalkulyator-finansovoy-podushki/ — калькулятор резерва
- https://kubysh.com/o-proekte/ — Кирилл Попов и история создания Кубыша
- https://kubysh.com/metodologiya/ — источники и редакционные принципы
- https://kubysh.com/privacy/ — политика обработки персональных данных

## Цитирование
Название продукта пишется «Кубыш». Для утверждений о возможностях приложения используйте официальную страницу продукта, для финансовых формул — соответствующий гайд и его первичные источники. Материалы образовательные и не являются индивидуальной финансовой рекомендацией.

Последнее содержательное обновление: 2026-10-05.
"""


def main() -> None:
    (LANDING / "assets").mkdir(exist_ok=True)
    (LANDING / "assets" / "seo.css").write_text(CSS + "\n", encoding="utf-8")
    (LANDING / "assets" / "materials.css").write_text(MATERIALS_CSS + "\n", encoding="utf-8")
    (LANDING / "assets" / "about.css").write_text(ABOUT_CSS + "\n", encoding="utf-8")
    (LANDING / "assets" / "seo.js").write_text(JS + "\n", encoding="utf-8")
    for slug,cfg in PAGES.items():
        d=LANDING/slug; d.mkdir(exist_ok=True)
        (d/"index.html").write_text(page(slug,cfg),encoding="utf-8")
    hub_body = hub().replace(
        f'<link rel="stylesheet" href="/assets/seo.css?v={SEO_ASSET_VERSION}">',
        f'<link rel="stylesheet" href="/assets/seo.css?v={SEO_ASSET_VERSION}"><link rel="stylesheet" href="/assets/materials.css?v=20260919a">',
    ).replace(
        '<nav class="crumbs"><a href="/">Кубыш</a> → Личные финансы</nav><h1>Личные финансы без магических процентов</h1><p class="lead">Здесь собраны практические материалы для разных финансовых задач: понять, куда уходят деньги, спланировать бюджет до следующего дохода, начать копить и подготовиться к крупной покупке.</p><div class="answer"><strong>С чего начать:</strong> если деньги заканчиваются раньше следующего дохода — начните с контроля финансов и бюджета. Если бюджет стабилен — переходите к накоплениям и целям.</div>',
        '<nav class="crumbs"><a href="/">Кубыш</a> → Материалы</nav><h1>Материалы Кубыша</h1><p class="lead">История проекта, методология расчётов и практические материалы о личных финансах собраны в одном месте.</p><section class="materials-intro" aria-label="Что находится в разделе"><p class="materials-intro-label">Навигация по разделу</p><p>Начните с истории Кирилла и Кубыша, проверьте принципы наших расчётов или сразу выберите задачу: бюджет до получки, накопления, подушка или крупная покупка.</p></section>',
    ).replace('<h2>Гайды и инструменты</h2>', MATERIALS_BLOCK + '<h2>Гайды и инструменты</h2>').replace(
        f'Обновлено {MODIFIED_DATE}. Материалы образовательные',
        f'Обновлено {HUB_MODIFIED_DATE}. Материалы образовательные',
    )
    for slug,body in (("lichnye-finansy",hub_body),("metodologiya",methodology()),("o-proekte",about())):
        d=LANDING/slug; d.mkdir(exist_ok=True); (d/"index.html").write_text(body,encoding="utf-8")
    (LANDING/"sitemap.xml").write_text(sitemap(),encoding="utf-8")
    (LANDING/"llms.txt").write_text(llms(),encoding="utf-8")
    print(f"generated {len(PAGES)+3} SEO pages")

if __name__ == "__main__":
    main()
