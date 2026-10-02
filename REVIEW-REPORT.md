# Screenshot Replacement Review

**Date:** 2026-10-02
**Reviewer:** Subagent (automated review)
**Scope:** 10 replacement slots across index.html and product-tour.html; retained/deferred slots on resources.html, company.html, use-cases.html.
**Source docs reviewed:** IMAGE-INVENTORY.md, SLOT-MAPPING.md, CHANGELOG-SCREENSHOTS.md, index.html, product-tour.html, resources.html, company.html, use-cases.html, `assets/img/product/` directory listing.
**Data-status assumption:** All selected screenshots treated as demo data (owner-confirmed 2026-10-02).

---

## Replacement Slot Results

| # | Page / Slot | Ledger | Asset Present | Alt Text | Demo Prefix | Message Fit | Verdict |
|---|---|---|---|---|---|---|---|
| 1 | index.html — hero | S34 | ✅ `learner-home.jpg` | ✅ Accurate; describes P³ journey | ✅ "Demo" | ✅ Broad product overview | **PASS** |
| 2 | index.html — Prepare card | S06 | ✅ `prepare-modules.jpg` | ✅ Structured preparation modules | ✅ "Demo" | ✅ Matches "structured learning" copy | **PASS** |
| 3 | index.html — Practise card | S04 | ✅ `practice-simulation.jpg` | ✅ Scenario + persona context | ✅ "Demo" | ✅ Matches rehearsal / AI coaching copy | **PASS** |
| 4 | index.html — Perform card | S01 | ✅ `practice-scoring.jpg` | ✅ Scoring + AI coaching feedback | ✅ "Demo" | ✅ Matches evidence / outcome-log copy | **PASS** |
| 5 | product-tour.html — overview | S34 | ✅ `learner-home.jpg` | ✅ P³ journey | ✅ "Demo" | ✅ Product overview hero | **PASS** |
| 6 | product-tour.html — Prepare (step 1) | S06 | ✅ `prepare-modules.jpg` | ✅ Preparation modules | ✅ "Demo" | ✅ "Flight manual" metaphor | **PASS** |
| 7 | product-tour.html — Practise (step 2) | S04 | ✅ `practice-simulation.jpg` | ✅ Practice simulation | ✅ "Demo" | ✅ "Simulator" metaphor | **PASS** |
| 8 | product-tour.html — coaching (step 3) | S01 | ✅ `practice-scoring.jpg` | ✅ Scoring + AI coaching feedback | ✅ "Demo" | ✅ "Instant coaching" copy | **PASS** |
| 9 | product-tour.html — readiness (step 4) | S14 | ✅ `team-readiness.jpg` | ✅ Team readiness view | ✅ "Demo" | ✅ "Prove readiness" copy | **PASS** |
| 10 | product-tour.html — manager (step 5) | S35 | ✅ `manager-home.jpg` | ✅ Manager home with team progress | ✅ "Demo" | ✅ "Observed outcomes" copy | **PASS** |

---

## Retained-Slot Checks

| Page | Slot | Expected | Actual | Verdict |
|---|---|---|---|---|
| resources.html | cs1-fhl-capital-cover.png | RETAIN / DEFER | ✅ Present, "Coming soon" label | **PASS** |
| resources.html | cs2-healthcare-cover.png | RETAIN / DEFER | ✅ Present, "Coming soon" label | **PASS** |
| resources.html | cs3-retail-cover.png | RETAIN / DEFER | ✅ Present, "Coming soon" label | **PASS** |
| company.html | about-team-scenario.png | RETAIN | ✅ Present | **PASS** |
| company.html | investors-vision-scenario.png | RETAIN | ✅ Present | **PASS** |
| company.html | partners-network-scenario.png | RETAIN | ✅ Present | **PASS** |
| use-cases.html | fs-advisor-scenario.png | RETAIN | ✅ Present | **PASS** |
| use-cases.html | uc1-healthcare-scenario.png | RETAIN | ✅ Present | **PASS** |
| use-cases.html | uc2-retail-drill.png | RETAIN | ✅ Present | **PASS** |
| use-cases.html | uc3-callcentre-coaching.png | RETAIN | ✅ Present | **PASS** |
| index.html | logo.gif, linkedin.png, p3-framework.jpg, mobile-app-real.jpg, hero-runner.jpg | RETAIN | ✅ All present | **PASS** |
| product-tour.html | logo.gif, linkedin.png | RETAIN | ✅ All present | **PASS** |

---

## Cross-Cutting Checks

### Demo-data claim safety
- ✅ All 10 replacement alt texts begin with **"Demo"** — no screenshot is presented as real customer data.
- ✅ SLOT-MAPPING.md prescribes "Label as demo UI; do not infer outcomes" for every slot.
- ✅ CHANGELOG-SCREENSHOTS.md records owner confirmation of demo-data status.
- ✅ product-tour.html "Proven in a real pilot" section cites FHL Capital statistics (90 %, 50 %, < 3 hrs) that are explicitly attributed to the named pilot and are **not** derived from any screenshot. Safe.
- ⚠️ **Advisory (non-blocking):** If a future archive contains real data, the "no crop / no redaction" decision documented in SLOT-MAPPING.md must be revisited before deployment.

### Alt-text accuracy
- ✅ Every alt text correctly describes the visual role of the screenshot in its slot.
- ✅ No alt text references specific customer names, metrics, or outcomes.

### Message appropriateness
- ✅ Hero / tour overview image (learner-home.jpg) matches the "broad product overview" narrative.
- ✅ P³ card images match their respective Prepare / Practise / Perform copy.
- ✅ Tour steps 1–5 images match their section headings and descriptions.
- ✅ No screenshot is used in a context that would imply validated performance claims.

### Resource / Company / Use-cases retention
- ✅ resources.html — all three case-study covers remain unchanged and are labelled "Coming soon."
- ✅ company.html — team, vision, and partner visuals remain unchanged.
- ✅ use-cases.html — all four sector illustrations remain unchanged.
- ✅ Rationale documented: generic product UI cannot substitute for named-customer evidence, people/strategy/partner representation, or sector-specific proof.

---

## Blocking Issues

**None.**

---

## Non-Blocking Advisories

1. resources.html case-cover alt texts are generic ("Concept mockup"). Acceptable while cards show "Coming soon," but alt text should be improved before case studies launch.
2. SLOT-MAPPING.md's "no crop / no redaction" stance is appropriate only while the source archive remains confirmed demo data. Revisit before any real-data archive is used.

---

## Final Verdict

### ✅ PASS — All 10 replacement slots pass. All retained/deferred slots confirmed intact. No blocking issues.
