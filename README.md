# Сайт Кубыша

Статика двух доменов и её раздача на проде.

| Домен | Папка | Что это |
|---|---|---|
| `kubysh.com` | `landing/` | лендинг, SEO-страницы, политика ПД, условия |
| `www.kubysh.com` | — | 301 на `https://kubysh.com` |
| `pay.kubysh.com` | `pay-site/` | личный кабинет, оплата, оферта, документы для Т-Банка |

API (`api.kubysh.com`) живёт в `pokirill/Finik-backend`, здесь его нет.
Страница оплаты ходит в API кросс-доменно: новый домен сайта требует правки CORS в бэкенде.

Подробности про кабинет, вход через Apple и CSP — в `pay-site/README.md`.

## Как устроено на сервере

Сервер `201.24.56.21`, каталог `/root/site`.

```
интернет → системный nginx :443 (certbot) ─┬─ kubysh.com, www, pay → 127.0.0.1:8082 → контейнер kubysh-site
                                           └─ api.kubysh.com       → 127.0.0.1:8080 → бэкенд
```

Файлы запекаются в образ при сборке, контейнер ничего не монтирует.
Заголовки (CSP, `Cache-Control`) задаются в `nginx/default.conf`.
Конфиг системного nginx лежит в `deploy/host-nginx.conf` для справки;
на сервере это `/etc/nginx/sites-enabled/kubysh-web.conf`, certbot дописывает в него TLS.

## Выкатка

После мержа в `main`:

```bash
ssh root@201.24.56.21 'cd /root/site && bash deploy/deploy.sh'
```

Скрипт подтягивает `main`, пересобирает контейнер (бэкенд не трогает)
и проверяет, что основные страницы обоих доменов отдают 200.

## Проверка перед пушем

```bash
python3 -m pytest -q
```

## SEO-страницы

Генератор — `scripts/generate_seo_cluster.py`, пишет в `landing/`.
