import json
import re
import shutil
import subprocess
from pathlib import Path
from xml.etree import ElementTree as ET
import pytest

ROOT = Path(__file__).resolve().parents[1]
LANDING = ROOT / "landing"
DATA = json.loads((ROOT / "scripts/seo_release_20261124.json").read_text(encoding="utf-8"))

def test_release_routes_and_calculators():
    urls = [e.text for e in ET.parse(LANDING / "sitemap.xml").findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
    hub = (LANDING / "lichnye-finansy/index.html").read_text(encoding="utf-8")
    calc_hub = (LANDING / "kalkulyatory/index.html").read_text(encoding="utf-8")
    kinds = set()
    for slug in [*DATA["pages"], *DATA["calculators"]]:
        page = (LANDING / slug / "index.html").read_text(encoding="utf-8")
        assert "https://kubysh.com/" + slug + "/" in urls
        if slug in DATA["pages"]:
            assert f'href="/{slug}/"' in hub
        kind = re.search(r'data-kb-calculator="([^"]+)"', page)
        if kind:
            kinds.add(kind.group(1))
            assert f'href="/{slug}/"' in calc_hub
            assert 'ym-hide-content' in page and 'ym-disable-keys' in page
            assert '/assets/calculators.js' in page
    assert kinds == {"daily","purchase","month","payday","savings","cushion","family","move","deadline","debt"}
    assert len(urls) == len(set(urls))
    assert not (LANDING / "pochemu-ne-hvataet-deneg-do-zarplaty").exists()

def test_js_calculations():
    node = shutil.which("node")
    if not node:
        pytest.skip("Node.js required")
    subprocess.run([node, str(Path(__file__).with_name("calculators.test.js"))], check=True)
