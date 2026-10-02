# Stock-photo integration — final review

Date: 2026-10-03 (Asia/Singapore)

## Executive summary

Five Pexels assets were downloaded, provenance-documented, and web-optimised. Four are rendered as clearly labelled illustrative accents on the homepage, Company, and Use Cases pages; the fifth remains an approved alternate in the stock asset library. Existing product screenshots, founder portraits, partner visuals, and named-customer case covers were not replaced. Local and Hostinger staging browser checks passed at desktop and mobile sizes. The staging deployment was backed up before sync. No outbound email or message was sent.

## Checklist

| Check | Result | Evidence |
|---|---|---|
| Every stock asset has a Pexels source and license | PASS | `assets/img/stock/SOURCE-MANIFEST.md` lists all five Pexels pages, photographers, CDN requests, license, hashes, and intended roles. |
| No RETAIN/REPLACE/DEFER image slot was altered | PASS | The diff only adds stock assets/figures and CSS; `product-tour.html`, `resources.html`, `partners.html`, and existing image references are unchanged. |
| No stock photo can be mistaken for a founder, team member, or named customer | PASS | Stock figures are separate from the founder grid and customer-resource cards; each has the visible stock-only caption. |
| Stock-image alt text is generic | PASS | All four rendered stock `alt` values describe scenes only and name no company, staff member, or customer. |
| Every rendered stock image has the stock-only caption/source marker | PASS | Four figures carry `data-stock-source="pexels"` and `Stock image for illustration only`; local and remote browser checks confirmed visibility. |
| Staging URLs serve the local content | PASS | `DEPLOY-LOG.md` records HTTP 200 for all changed pages, CSS, five JPGs, and the manifest; remote byte sizes match local derivatives. |
| No messages or emails were sent | PASS | No outbound messaging or email tool was used. |

## Deviations and residuals

- `stock-19895721-workshop.jpg` is stored as an approved alternate but is not placed in the current page layout, avoiding visual overload.
- `LOCAL-REVIEW.md` and review screenshots remain repository QA artifacts and were not exposed in the public web root.
- axe found one pre-existing serious `link-in-text-block` warning on the Company investor mailto link; no stock element was implicated and it was left outside this photo-only change.

## Attestation

No founder/customer misrepresentation risk.
