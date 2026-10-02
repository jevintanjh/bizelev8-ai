# Stock-photo staging deployment

Date: 2026-10-03 (Asia/Singapore)

## Target

- Hostinger staging VPS: `72.62.73.170`
- Web root: `/var/www/bizelev8`
- Deployment scope: `company.html`, `index.html`, `use-cases.html`, `styles.css`, `assets/img/stock/*.jpg`, and `assets/img/stock/SOURCE-MANIFEST.md`
- Backup: `/root/backups/bizelev8-stock-accent-20261003-0117`
- Source commit: `cf8356f` (`feat: add illustrative stock photo accents`)

`LOCAL-REVIEW.md` and the rendered review screenshots remain repository QA artifacts and were not copied into the public web root.

## Sync and verification

- Remote `nginx -t`: PASS
- Rsync/SFTP sync: PASS
- Remote HTML/CSS and stock image URLs: HTTP 200
- Remote `company.html` stock markers: 2
- Remote `use-cases.html` stock markers: 1
- Remote browser smoke test: 3 pages × desktop/mobile = 6 checks; all HTTP 200, no broken images, no page errors, no horizontal overflow, and all stock captions/source attributes present.

| Remote path | HTTP status | Bytes |
|---|---:|---:|
| `index.html` | 200 | 11276 |
| `company.html` | 200 | 7885 |
| `use-cases.html` | 200 | 10003 |
| `styles.css` | 200 | 13108 |
| `assets/img/stock/stock-6457537-collaboration.jpg` | 200 | 144046 |
| `assets/img/stock/stock-18999540-training.jpg` | 200 | 242478 |
| `assets/img/stock/stock-19895721-workshop.jpg` | 200 | 218606 |
| `assets/img/stock/stock-7845344-meeting.jpg` | 200 | 121616 |
| `assets/img/stock/stock-5668828-handshake.jpg` | 200 | 163721 |
| `assets/img/stock/SOURCE-MANIFEST.md` | 200 | 3171 |
