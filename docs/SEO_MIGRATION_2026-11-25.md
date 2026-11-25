# November SEO migration (review required)
Source: fullbyte8179/Kubysh-web@346a6519df7aa210f9bf3b2fa7a9b386a52a6d47 (PR #2).

- 24 source guide routes including the purchase guide; 23 distinct new guide routes, one overlapping payday-shortfall guide folded into existing ne-hvataet-deneg-do-zarplaty. Plus credit burden and calculator hub. Original overlapping article retained in generator JSON for review.
- 10 calculator topics; existing savings and cushion redirect URLs are not recreated. Existing target page content retained except replacement of the old calculator widget where applicable.
- Generator extension recreates the new HTML and adds links to materials hub, sitemap and llms.txt. No payment, nginx, legal, root landing or analytics changes.
- Before merging: run generator and inspect git diff, pytest, node tests, Docker smoke, review intent overlap and bank/product claims across all new content; confirm masked calculator inputs/output in Metrika browser recordings, review mobile rendering and add homepage navigation if desired. Existing baseline product-definition contract may already be stale; do not weaken it to force CI green.
- This is a review branch, not a production deployment.
