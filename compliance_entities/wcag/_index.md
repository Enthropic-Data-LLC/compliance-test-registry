# WCAG 2.2 / Section 508 — Digital Accessibility

**Registry version:** 2026.05
**Last updated:** 2026-05-20
**Scope:** Accessibility of web content and software interfaces for people with disabilities; WCAG 2.2 is the international standard; Section 508 is the US federal requirement (incorporates WCAG 2.0 Level AA as of 2018 refresh)
**Authority:** W3C Web Accessibility Initiative (WAI) publishes WCAG; US Access Board + GSA enforce Section 508; DOJ enforces ADA Title II/III digital accessibility; EU enforces EN 301 549 (adopts WCAG 2.1)
**Enforcing context (Section 508):** US federal agencies and their contractors/vendors; US state agencies (Section 504); ADA Title II (state/local governments) and Title III (places of public accommodation) — pending DOJ rulemaking
**Current edition:** WCAG 2.2 (October 2023); WCAG 3.0 in development

---

## Summary

| Metric | Count |
|---|---|
| WCAG 2.2 principles | 4 (POUR) |
| WCAG 2.2 guidelines | 13 |
| WCAG 2.2 success criteria | 87 total (78 inherited from 2.1, 9 new in 2.2) |
| Conformance levels | 3 (A / AA / AAA) |
| Section 508 required level | WCAG 2.0 Level AA (federal) |
| EN 301 549 required level | WCAG 2.1 Level AA (EU) |
| Sections parsed (individual files) | 0 (index only) |
| Fully automated (DETERMINISTIC) | Moderate — automated tools catch ~30-40% of issues |
| Partial automation (PARAMETERIZED) | Moderate — requires testing context |
| Human-determination required (CONTESTED) | High — most success criteria require human judgment |
| Open assumptions | 0 |

---

## 4 WCAG principles (POUR)

| Principle | Description |
|---|---|
| Perceivable | Information and UI components must be presentable to users in ways they can perceive |
| Operable | UI components and navigation must be operable |
| Understandable | Information and UI operation must be understandable |
| Robust | Content must be interpretable by a wide variety of user agents, including assistive technologies |

---

## Success criteria confidence map (selected high-impact criteria)

### Perceivable

| SC | Level | Requirement | Confidence |
|---|---|---|---|
| 1.1.1 Non-text Content | A | All non-text content has text alternative | PARAMETERIZED — alt text quality is judgment-based |
| 1.2.1 Audio-only / Video-only | A | Prerecorded media has text transcript | DETERMINISTIC — transcript exists or doesn't |
| 1.2.2 Captions (Prerecorded) | A | Captions provided for prerecorded audio in video | DETERMINISTIC — captions present/absent |
| 1.2.3 Audio Description | A | Audio description or media alternative for video | DETERMINISTIC — exists or not |
| 1.3.1 Info and Relationships | A | Structural information conveyed through text and programmatic markup | PARAMETERIZED |
| 1.4.1 Use of Color | A | Color not used as sole means of conveying information | PARAMETERIZED |
| 1.4.3 Contrast (Minimum) | AA | Text has 4.5:1 contrast ratio (3:1 for large text) | DETERMINISTIC — measurable ratio |
| 1.4.4 Resize Text | AA | Text resizable to 200% without loss of content | DETERMINISTIC — testable |
| 1.4.11 Non-text Contrast | AA (2.1) | UI components have 3:1 contrast | DETERMINISTIC — measurable |
| 1.4.13 Content on Hover/Focus | AA (2.1) | Hover/focus content dismissible, hoverable, persistent | PARAMETERIZED |

### Operable

| SC | Level | Requirement | Confidence |
|---|---|---|---|
| 2.1.1 Keyboard | A | All functionality available via keyboard | PARAMETERIZED — requires testing |
| 2.1.2 No Keyboard Trap | A | Focus can always be moved away from component | DETERMINISTIC — binary |
| 2.4.1 Bypass Blocks | A | Mechanism to bypass repeated blocks (skip nav) | DETERMINISTIC — exists or not |
| 2.4.3 Focus Order | A | Focusable components in meaningful sequence | PARAMETERIZED |
| 2.4.4 Link Purpose | A | Link purpose determinable from link text or context | PARAMETERIZED |
| 2.4.7 Focus Visible | AA | Keyboard focus indicator visible | PARAMETERIZED |
| 2.4.11 Focus Appearance | AA (2.2) | Focus indicator meets minimum size and contrast | DETERMINISTIC — measurable |
| 2.5.3 Label in Name | A (2.1) | Accessible name contains visible label text | DETERMINISTIC — testable |

### Understandable

| SC | Level | Requirement | Confidence |
|---|---|---|---|
| 3.1.1 Language of Page | A | Default human language identified in code | DETERMINISTIC — `lang` attribute present/absent |
| 3.2.1 On Focus | A | No context change on focus | PARAMETERIZED |
| 3.3.1 Error Identification | A | Input errors described in text | PARAMETERIZED |
| 3.3.2 Labels or Instructions | A | Labels or instructions provided for user input | PARAMETERIZED |

### Robust

| SC | Level | Requirement | Confidence |
|---|---|---|---|
| 4.1.1 Parsing | A | HTML/XML valid (Note: deprecated in 2.2) | — |
| 4.1.2 Name, Role, Value | A | All UI components have accessible name, role, state | DETERMINISTIC — testable with accessibility tree |
| 4.1.3 Status Messages | AA (2.1) | Status messages can be programmatically determined | PARAMETERIZED |

---

## WCAG 2.2 new success criteria (9 new vs. 2.1)

| SC | Level | Requirement |
|---|---|---|
| 2.4.11 Focus Appearance | AA | Focus indicator minimum size (≥ perimeter of component) + contrast (3:1) |
| 2.4.12 Focus Appearance (Enhanced) | AAA | — |
| 2.4.13 Focus Appearance (Minimum) (renumbered) | — | — |
| 2.5.7 Dragging Movements | AA | All drag functionality has single-pointer alternative |
| 2.5.8 Target Size (Minimum) | AA | Target size ≥ 24×24 CSS pixels (with exceptions) |
| 3.2.6 Consistent Help | A | Help mechanism in consistent location across pages |
| 3.3.7 Redundant Entry | A | Information entered earlier auto-populated or available to select |
| 3.3.8 Accessible Authentication (Minimum) | AA | No cognitive function test required for authentication |
| 3.3.9 Accessible Authentication (Enhanced) | AAA | — |

---

## Conformance levels

| Level | Description | When required |
|---|---|---|
| Level A | Minimum (25 criteria) | Baseline |
| Level AA | Standard (25 A + 20 AA = 45 criteria) | Section 508 / ADA enforcement / EN 301 549 |
| Level AAA | Enhanced (all 87) | Aspirational; not required for general conformance |

---

## Automated vs. manual testing split

| Detection method | % of WCAG issues detectable |
|---|---|
| Automated tools (axe, WAVE, Lighthouse) | ~30–40% |
| Manual keyboard testing | Additional ~20% |
| Screen reader testing | Additional ~20% |
| Cognitive/usability evaluation | Remaining ~20% |

Full WCAG conformance requires automated + manual + assistive technology testing.

---

## Key DETERMINISTIC thresholds

| Criterion | Threshold |
|---|---|
| Color contrast (normal text) | 4.5:1 minimum |
| Color contrast (large text ≥ 18pt or 14pt bold) | 3:1 minimum |
| Non-text contrast (UI components) | 3:1 minimum |
| Focus indicator contrast | 3:1 minimum |
| Minimum target size (2.5.8) | 24×24 CSS pixels |
| Captions for prerecorded video | Required |
| Skip navigation link | Required |

---

## Cross-standard dependencies

| Shared artifact | Frameworks | Notes |
|---|---|---|
| Accessibility testing | WCAG 2.2, Section 508, EN 301 549, ADA Title II/III | Same test results support all four; different legal basis |
| VPAT / ACR (Accessibility Conformance Report) | Section 508 (US federal procurement), EN 301 549 (EU public sector) | VPAT documents WCAG conformance for procurement |
| Cognitive accessibility | WCAG 2.2 SC 3.3.8, COGA (Cognitive Accessibility Guidance), ADA Titles II/III | |
| Mobile accessibility | WCAG 2.2 SC 2.5.x series, EN 301 549 §11.x (mobile) | Same criteria; mobile adds gesture-specific criteria |
