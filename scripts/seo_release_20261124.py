"""Integrate the November SEO release without replacing existing page templates."""
import json
import re
from pathlib import Path

ASSETS = "<link rel=\"stylesheet\" href=\"/assets/calculators.css?v=20261124\"><script defer src=\"/assets/calculators.js?v=20261124\"></script>"
DATE = "2026-11-24"

def apply_release(landing: Path) -> None:
    data = json.loads(Path(__file__).with_suffix(".json").read_text(encoding="utf-8"))
    def edit(path, transform):
        p = landing / path
        old = p.read_text(encoding="utf-8")
        new = transform(old)
        if new != old:
            p.write_text(new, encoding="utf-8")
    for slug, body in data["pages"].items():
        p = landing / slug / "index.html"
        p.parent.mkdir(exist_ok=True)
        p.write_text(body, encoding="utf-8")
    for slug, block in data["calculators"].items():
        def calc(body):
            if 'data-kb-calculator=' in body:
                return body
            body = body.replace("</head>", ASSETS + "</head>", 1)
            body, n = re.subn(r'<section class="tool"[\s\S]*?</section>', lambda _: block, body, count=1)
            if not n:
                body, n = re.subn(r'<p class="lead">[\s\S]*?</p>', lambda m: m.group(0) + block, body, count=1)
            if not n:
                raise ValueError("Calculator insertion failed: " + slug)
            return body
        edit(slug + "/index.html", calc)
    edit("ne-hvataet-deneg-do-zarplaty/index.html", lambda s: s if 'id="additional-budget-guide"' in s else s.replace('<section class="faq">', data["duplicate_block"] + '<section class="faq">', 1))
    edit("lichnye-finansy/index.html", lambda s: s if 'id="seo-release-20261124"' in s else s.replace("</main>", data["hub_block"] + "</main>", 1))
    def sitemap(s):
        for slug in [*data["calculators"], "ne-hvataet-deneg-do-zarplaty", "lichnye-finansy"]:
            s = re.sub(r'(<loc>https://kubysh\.com/' + re.escape(slug) + r'/</loc><lastmod>)[^<]+', lambda m: m.group(1) + DATE, s)
        for c in data["cards"]:
            url = "https://kubysh.com/" + c["slug"] + "/"
            if "<loc>" + url + "</loc>" not in s:
                s = s.replace("</urlset>", "  <url><loc>" + url + "</loc><lastmod>" + DATE + "</lastmod></url>\n</urlset>")
        return s
    edit("sitemap.xml", sitemap)
    edit("llms.txt", lambda s: s if "## Новые гайды и калькуляторы" in s else s.replace("## Цитирование", data["llms_block"] + "\n## Цитирование").replace("Последнее содержательное обновление: 2026-11-12.", "Последнее содержательное обновление: 2026-11-24."))
