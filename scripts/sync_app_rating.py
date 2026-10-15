#!/usr/bin/env python3
"""Sync the App Store rating on the home page with the real one from iTunes lookup.

Updates `aggregateRating` in the SoftwareApplication JSON-LD and the visible
"★ X,X в App Store" notes. If lookup is unavailable or the app has no ratings,
removes `aggregateRating`: no rating in the markup is better than a made-up one.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from urllib.request import urlopen


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "landing" / "index.html"
LOOKUP = "https://itunes.apple.com/lookup?id=6778792103&country=ru"

AUDIENCE_END = '    "audienceType": "Люди с регулярной зарплатой и iPhone"\n   }'
RATING_BLOCK = re.compile(r',\n   "aggregateRating": \{\n.*?\n   \}(?=\n  \})', re.S)
VISIBLE = re.compile(r"★ \d,\d в App Store")


def fetch_rating() -> tuple[float, int] | None:
    try:
        with urlopen(LOOKUP, timeout=15) as response:
            results = json.load(response).get("results") or []
    except (OSError, ValueError):
        return None
    if not results:
        return None
    value, count = results[0].get("averageUserRating"), results[0].get("userRatingCount")
    if not value or not count:
        return None
    return round(float(value), 1), int(count)


def apply(text: str, rating: tuple[float, int] | None) -> str:
    text = RATING_BLOCK.sub("", text)
    if rating is None:
        return text
    value, count = rating
    block = (
        ',\n   "aggregateRating": {\n'
        '    "@type": "AggregateRating",\n'
        f'    "ratingValue": "{value:.1f}",\n'
        f'    "ratingCount": "{count}",\n'
        '    "bestRating": "5",\n'
        '    "worstRating": "1"\n'
        "   }"
    )
    if AUDIENCE_END not in text:
        raise SystemExit("anchor for aggregateRating not found in landing/index.html")
    text = text.replace(AUDIENCE_END, AUDIENCE_END + block, 1)
    return VISIBLE.sub(f"★ {value:.1f}".replace(".", ",") + " в App Store", text)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--remove", action="store_true", help="drop aggregateRating without lookup")
    args = parser.parse_args()
    rating = None if args.remove else fetch_rating()
    INDEX.write_text(apply(INDEX.read_text(encoding="utf-8"), rating), encoding="utf-8")
    if rating:
        print(f"aggregateRating: {rating[0]:.1f}, {rating[1]} ratings")
    else:
        print("aggregateRating removed: lookup unavailable or no ratings")


if __name__ == "__main__":
    main()
