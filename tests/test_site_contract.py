from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
LANDING = ROOT / "landing"
PAY = ROOT / "pay-site"


def test_required_files_exist():
    for path in (
        "index.html",
        "robots.txt",
        "sitemap.xml",
        "llms.txt",
        "assets/seo.css",
        "assets/seo.js",
        "lichnye-finansy/index.html",
        "kontrol-finansov/index.html",
        "kalkulyator-nakopleniy/index.html",
        "kalkulyator-finansovoy-podushki/index.html",
    ):
        assert (LANDING / path).is_file(), path


def test_main_build_marker_and_metrica():
    text = (LANDING / "index.html").read_text(encoding="utf-8")
    assert 'meta name="build" content="' in text
    assert "44147844" in text


def test_main_landing_local_assets_exist():
    text = (LANDING / "index.html").read_text(encoding="utf-8")
    references = set(re.findall(r'(?:src|href)=["\']([^"\']+)["\']', text))
    references.update(re.findall(r'url\((?:["\'])?([^\)"\']+)', text))
    asset_suffixes = (".css", ".ico", ".jpeg", ".jpg", ".js", ".png", ".webp", ".woff", ".woff2")

    for reference in references:
        clean = reference.split("#", 1)[0].split("?", 1)[0].strip()
        if clean.startswith(("data:", "http://", "https://", "mailto:", "tel:", "javascript:")):
            continue
        if not clean.lower().endswith(asset_suffixes):
            continue
        assert (LANDING / clean.lstrip("/")).is_file(), reference


def test_seo_cluster_has_unique_canonicals_and_sitemap_entries():
    sitemap = (LANDING / "sitemap.xml").read_text(encoding="utf-8")
    required = (
        "/kontrol-finansov/",
        "/uchet-rashodov-i-dohodov/",
        "/planirovanie-byudzheta/",
        "/kak-raspredelit-zarplatu/",
        "/kak-ekonomit-dengi/",
        "/kak-kopit-dengi/",
        "/kalkulyator-nakopleniy/",
        "/kalkulyator-finansovoy-podushki/",
        "/kak-nakopit-na-kvartiru/",
        "/kak-nakopit-na-mashinu/",
        "/kak-nakopit-na-otpusk/",
        "/kak-nakopit-na-telefon/",
        "/kak-nakopit-na-svadbu/",
        "/prilozhenie-dlya-kontrolya-rashodov/",
        "/finansovyy-stress/",
        "/byudzhet-na-mesyats/",
    )
    for path in required:
        assert f"https://kubysh.com{path}" in sitemap

    canonicals = []
    for page in LANDING.glob("*/index.html"):
        text = page.read_text(encoding="utf-8")
        match = re.search(r'<link rel="canonical" href="([^"]+)"', text)
        if match:
            canonicals.append(match.group(1))
    assert canonicals
    assert len(canonicals) == len(set(canonicals))


def test_generated_seo_pages_track_appstore_clicks():
    js = (LANDING / "assets/seo.js").read_text(encoding="utf-8")
    assert "seo_appstore_click" in js
    assert "44147844" in js


def test_nginx_routes_hosts_explicitly():
    text = (ROOT / "nginx/default.conf").read_text(encoding="utf-8")
    for expected in (
        "listen 80 default_server;",
        "location = /healthz",
        "server_name www.kubysh.com;",
        "return 301 https://kubysh.com$request_uri;",
        "server_name kubysh.com;",
        "root /srv/www/kubysh;",
        'Cache-Control "no-cache, must-revalidate"',
        "server_name pay.kubysh.com;",
        "root /srv/www/pay;",
        'Cache-Control "no-store, must-revalidate"',
        "Content-Security-Policy",
    ):
        assert expected in text
    assert "'unsafe-inline'; img-src" in text  # only style-src may be inline
    assert "script-src 'self' https://appleid.cdn-apple.com;" in text


def test_pay_site_required_pages_exist():
    for path in (
        "index.html",
        "account/index.html",
        "offer/index.html",
        "recurrent/index.html",
        "privacy/index.html",
        "pay/success/index.html",
        "pay/fail/index.html",
        "robots.txt",
        "assets/pay-config.js",
    ):
        assert (PAY / path).is_file(), path


def test_pay_account_has_app_return_and_no_public_requisites():
    text = (PAY / "account/index.html").read_text(encoding="utf-8")
    assert 'href="kubyshka://"' in text
    active = text.split('<section id="state-active"', 1)[1].split("</section>", 1)[0]
    assert "Условия:" not in active


def test_success_page_can_return_to_app():
    text = (PAY / "pay/success/index.html").read_text(encoding="utf-8")
    assert 'href="kubyshka://"' in text
    assert "https://apps.apple.com/app/id6778792103" in text


def test_transactional_pages_do_not_publish_business_requisites():
    for page in (
        PAY / "index.html",
        PAY / "account/index.html",
        PAY / "pay/success/index.html",
        PAY / "pay/fail/index.html",
    ):
        text = page.read_text(encoding="utf-8")
        for marker in ("ОГРНИП", "ИНН ", "ИП Попов"):
            assert marker not in text, f"{marker!r} leaked into {page}"


def test_account_loads_apple_sdk_before_click_handler():
    html = (PAY / "account/index.html").read_text(encoding="utf-8")
    assert "appleid.auth.js" in html
    assert "/assets/pay-auth.js" in html
    assert html.index("appleid.auth.js") < html.index("/assets/pay-auth.js")

    auth_js = (PAY / "assets/pay-auth.js").read_text(encoding="utf-8")
    assert "sdkReady()" in auth_js
    assert "sdkReady()\n      ? beginAppleSignIn" in auth_js


def test_pay_site_scripts_are_never_inline():
    for page in PAY.rglob("*.html"):
        text = page.read_text(encoding="utf-8")
        for tag in re.findall(r"<script\b[^>]*>", text):
            assert "src=" in tag, f"inline script in {page}"
