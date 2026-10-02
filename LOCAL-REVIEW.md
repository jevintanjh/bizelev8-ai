# Stock-photo integration — local review

Date: 2026-10-03 (Asia/Singapore)

## Browser verification

Local server: `python3 -m http.server 8787` serving this repository.

| Page | Desktop 1440px | Mobile 390px | Stock accents | Broken images | Horizontal overflow | Page errors |
|---|---:|---:|---:|---:|---:|---:|
| `index.html` | PASS / HTTP 200 | PASS / HTTP 200 | 1 | 0 | 0 | 0 |
| `company.html` | PASS / HTTP 200 | PASS / HTTP 200 | 2 | 0 | 0 | 0 |
| `use-cases.html` | PASS / HTTP 200 | PASS / HTTP 200 | 1 | 0 | 0 | 0 |

Every stock image loaded at 1600×1067, carries `class="stock-accent"` and `data-stock-source="pexels"`, has generic scene-only alt text, and has a visible `Stock image for illustration only` caption. All images on the three checked pages have non-empty alt attributes.

## Accessibility

- axe-core 4.10.2 WCAG 2A/2AA scan: 0 critical violations on all three pages and 0 violations attached to any stock accent.
- `index.html`: 0 violations.
- `company.html`: 1 pre-existing serious `link-in-text-block` warning on the investor contact mailto link; it is outside this photo change and does not target a stock element.
- `use-cases.html`: 0 violations.

## Photo-context audit

- PASS — stock photos are illustrative accents and do not replace any product, founder, partner, or case-study image.
- PASS — no stock image is inside the founder/team card grid or the named-customer resource cards.
- PASS — stock images use generic alt text and do not name Bizelev8 staff or customers.
- PASS — each rendered stock image has the visible stock-only caption.
- PASS — the Company collaboration image is in the About section, separated from the following Team section by a section boundary and its own heading; it cannot be read as a founder portrait.
- PASS — the handshake image is in the Investors section and the meeting image is in a separate homepage accent section.

## Review screenshots

Rendered desktop stock-accent crops are stored under `assets/img/stock/review-screenshots/`:

- `index-1-desktop.png`
- `company-1-desktop.png`
- `company-2-desktop.png`
- `use-cases-1-desktop.png`
