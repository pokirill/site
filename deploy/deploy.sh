#!/usr/bin/env bash
# Update kubysh.com and pay.kubysh.com on the production server.
# Run on the server: cd /root/site && bash deploy/deploy.sh
set -euo pipefail
cd "$(dirname "$0")/.."

if [ -n "$(git status --porcelain)" ]; then
  echo "working tree is dirty, refusing to deploy" >&2
  exit 1
fi

git pull --ff-only origin main
docker compose up -d --build

for i in $(seq 1 30); do
  if curl -fsS http://127.0.0.1:8082/healthz >/dev/null; then break; fi
  sleep 1
done

fail=0
check() {
  local host=$1 path=$2 code
  code=$(curl -s -o /dev/null -w '%{http_code}' -H "Host: $host" "http://127.0.0.1:8082$path")
  printf '%s %s%s\n' "$code" "$host" "$path"
  [ "$code" = 200 ] || fail=1
}
for p in / /sitemap.xml /robots.txt /privacy/ /terms/ /kontrol-finansov/; do check kubysh.com "$p"; done
for p in / /account/ /offer/ /recurrent/ /privacy/ /pay/success/ /pay/fail/; do check pay.kubysh.com "$p"; done
exit $fail
