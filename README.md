# bizelev8-ai

Static marketing website for bizElev8 (P³ CUE). Built from Esleen's skeleton (DEC-055, 2026-08-30).

## Structure
- Root: static HTML/CSS (index, product-tour, use-cases, pricing, company, resources, login)
- `assets/` — images, fonts
- `styles.css` — global styles

## Deployment
Deployed to Hostinger `public_html/` via SFTP from the JervonClaw VPS.

## Local preview
`python3 -m http.server 8080` in repo root.

## Notes
- Login button redirects to `app.bizelev8.ai` (product app, external)
- Live site (pre-cutover): Wix still serving bizelev8.ai
