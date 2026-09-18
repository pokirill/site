#!/usr/bin/env python3
"""Notify IndexNow participants about canonical URLs from the sitemap."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.request import Request, urlopen
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[1]
SITEMAP = ROOT / "landing" / "sitemap.xml"
HOST = "kubysh.com"
KEY = "e71cfcc509bb37c30ca5eafc01a4bb9a"
KEY_LOCATION = f"https://{HOST}/{KEY}.txt"
ENDPOINT = "https://api.indexnow.org/indexnow"


def canonical_urls() -> list[str]:
    root = ElementTree.parse(SITEMAP).getroot()
    namespace = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    return [node.text for node in root.findall("s:url/s:loc", namespace) if node.text]


def payload() -> dict[str, object]:
    return {
        "host": HOST,
        "key": KEY,
        "keyLocation": KEY_LOCATION,
        "urlList": canonical_urls(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    body = json.dumps(payload(), ensure_ascii=False).encode("utf-8")
    if args.dry_run:
        print(body.decode("utf-8"))
        return
    request = Request(ENDPOINT, data=body, headers={"Content-Type": "application/json; charset=utf-8"})
    with urlopen(request, timeout=30) as response:
        print(f"IndexNow accepted {len(canonical_urls())} URLs: HTTP {response.status}")


if __name__ == "__main__":
    main()
