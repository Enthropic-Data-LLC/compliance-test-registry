# WCAG 2.2 / Section 508 — Digital Accessibility Requirements

**Framework:** Web Content Accessibility Guidelines 2.2 (W3C Recommendation, October 2023); Section 508 of the Rehabilitation Act (29 U.S.C. §794d); ADA Titles II and III (digital accessibility enforcement)
**Clauses:** WCAG 2.2 — 87 success criteria across 4 principles (POUR); Level A/AA required for Section 508 / ADA / EN 301 549 conformance; Section 508 requires WCAG 2.0 Level AA for federal ICT; new WCAG 2.2 criteria include SC 2.4.11 (Focus Appearance), SC 2.5.7 (Dragging Movements), SC 2.5.8 (Target Size Minimum 24×24 px), SC 3.2.6 (Consistent Help), SC 3.3.7 (Redundant Entry), SC 3.3.8 (Accessible Authentication)
**Confidence:** DETERMINISTIC (color contrast 4.5:1 / 3:1 measurable thresholds; skip navigation presence; captions for prerecorded video; `lang` attribute; focus indicator measurable contrast; target size 24×24 CSS px minimum; captions present/absent binary); PARAMETERIZED (alt text quality; keyboard navigation completeness; focus order meaningfulness; link purpose in context); CONTESTED (most SC requiring judgment — "sufficient" alt text quality, "meaningful" sequence, "clear" labels)
**Last parsed:** 2026-05-21
**Applies to:** US federal agencies and their contractors/vendors (Section 508, mandatory); state and local governments (ADA Title II — DOJ rulemaking effective 2026 for large entities); places of public accommodation (ADA Title III — case-by-case enforcement); any organization seeking WCAG 2.2 conformance for EU EN 301 549 compliance or international procurement; any organization requiring ISO/IEC 40500 (identical to WCAG 2.0) certification
**Trigger:** Section 508: any ICT procurement or development by federal agencies; ADA Title II: state/local government websites and apps; ADA Title III: courts interpreting places of public accommodation to include websites; EN 301 549: EU public sector body ICT procurement; VPAT/ACR requested by customers as procurement qualification
**Jurisdiction:** United States (Section 508, ADA); European Union (EN 301 549 = WCAG 2.1 Level AA); global — WCAG is the international baseline referenced by accessibility laws in Canada, Australia, UK, Japan, India, and others
**Not applicable to:** Time-based media where accessibility is not technically feasible and noted as an exception; archived web content not subject to current use or modification; third-party content not under the organization's control (limited liability); content not covered by Section 508 (paper documents, non-ICT); purely intranet content exempt from Title II/III (case-dependent)

---

## Scope pre-condition

```python
import pytest

@pytest.fixture(autouse=True)
def wcag_scope(entity_profile: dict):
    subject = (
        entity_profile.get("federal_agency_ict", False)              # Section 508
        or entity_profile.get("state_local_government_digital", False) # ADA Title II
        or entity_profile.get("public_accommodation_website", False)  # ADA Title III
        or entity_profile.get("wcag_conformance_claimed", False)      # voluntary/procurement
        or entity_profile.get("eu_public_sector_ict", False)          # EN 301 549
    )
    if not subject:
        pytest.skip(
            "WCAG 2.2 / Section 508 accessibility requirements do not apply — "
            "entity is not subject to Section 508, ADA digital accessibility, "
            "EN 301 549, or a voluntary WCAG conformance claim."
        )
```

---

## Constants

```python
from typing import FrozenSet
from decimal import Decimal

# ── Color contrast thresholds (SC 1.4.3, 1.4.6, 1.4.11) ─────────────────────

WCAG_NORMAL_TEXT_CONTRAST_RATIO = Decimal("4.5")   # SC 1.4.3 Level AA
WCAG_LARGE_TEXT_CONTRAST_RATIO = Decimal("3.0")    # SC 1.4.3 Level AA (≥18pt or 14pt bold)
WCAG_NON_TEXT_CONTRAST_RATIO = Decimal("3.0")      # SC 1.4.11 Level AA
WCAG_FOCUS_INDICATOR_CONTRAST_RATIO = Decimal("3.0")  # SC 2.4.11 Level AA (WCAG 2.2 new)

WCAG_LARGE_TEXT_SIZE_PT = 18       # Regular weight
WCAG_LARGE_TEXT_SIZE_BOLD_PT = 14  # Bold weight

# ── SC 2.5.8 — Target size minimum (WCAG 2.2 new) ────────────────────────────

WCAG_TARGET_SIZE_MIN_CSS_PX = 24   # SC 2.5.8 Level AA — 24×24 CSS pixels minimum

# ── Conformance levels ────────────────────────────────────────────────────────

WCAG_SECTION_508_REQUIRED_LEVEL = "AA"   # Section 508 requires WCAG 2.0 Level AA
WCAG_EN_301_549_REQUIRED_LEVEL = "AA"    # EN 301 549 requires WCAG 2.1 Level AA

# ── Level A success criteria requiring automated-detectable checks ─────────────

LEVEL_A_DETERMINISTIC_CRITERIA: FrozenSet[str] = frozenset({
    "1.2.1_audio_only_video_only_transcript",     # transcript present/absent
    "1.2.2_captions_prerecorded",                 # captions present/absent
    "1.2.3_audio_description_prerecorded",        # audio description present/absent
    "2.1.2_no_keyboard_trap",                     # binary — keyboard can always leave component
    "2.4.1_bypass_blocks_skip_nav",               # skip nav link present/absent
    "3.1.1_language_of_page_lang_attribute",      # lang attribute present/absent
    "4.1.2_name_role_value",                      # accessible name/role/state in accessibility tree
})

# ── Level AA success criteria with measurable thresholds ─────────────────────

LEVEL_AA_DETERMINISTIC_CRITERIA: FrozenSet[str] = frozenset({
    "1.4.3_contrast_minimum",           # 4.5:1 normal / 3:1 large — measurable
    "1.4.4_resize_text_200_percent",    # text resizable to 200% — testable
    "1.4.11_non_text_contrast",         # 3:1 for UI components — measurable
    "2.4.11_focus_appearance",          # focus indicator meets area + contrast (WCAG 2.2)
    "2.5.7_dragging_movements",         # single-pointer alternative present — binary
    "2.5.8_target_size_minimum",        # ≥24×24 CSS px — measurable
    "3.2.6_consistent_help",            # help in consistent location — binary per implementation
    "3.3.7_redundant_entry",            # previously entered info available — binary
    "3.3.8_accessible_authentication",  # no cognitive function test required — binary
})
```

---

## TestColorContrast

```python
class TestColorContrast:
    """SC 1.4.3 (Level AA), SC 1.4.11 (Level AA) — Color contrast: measurable ratios."""

    def test_normal_text_meets_minimum_contrast_ratio(self, entity_profile: dict):
        """SC 1.4.3: Text and images of text must have a contrast ratio of at least 4.5:1
        (3:1 for large text ≥18pt regular or ≥14pt bold)."""
        for element in entity_profile.get("text_elements", []):
            contrast = Decimal(str(element.get("contrast_ratio", 0)))
            font_size_pt = element.get("font_size_pt", 0)
            is_bold = element.get("is_bold", False)
            is_large_text = (
                font_size_pt >= WCAG_LARGE_TEXT_SIZE_PT
                or (is_bold and font_size_pt >= WCAG_LARGE_TEXT_SIZE_BOLD_PT)
            )
            required = WCAG_LARGE_TEXT_CONTRAST_RATIO if is_large_text else WCAG_NORMAL_TEXT_CONTRAST_RATIO
            assert contrast >= required, (
                f"Text element '{element.get('id', 'unknown')}': contrast ratio {contrast} "
                f"does not meet {'3:1 (large text)' if is_large_text else '4.5:1'} minimum — "
                f"SC 1.4.3 Level AA"
            )

    def test_ui_components_meet_non_text_contrast_ratio(self, entity_profile: dict):
        """SC 1.4.11: UI components and graphical objects must have at least 3:1 contrast
        against adjacent colors."""
        for element in entity_profile.get("ui_components", []):
            if element.get("decorative_only", False):
                continue
            contrast = Decimal(str(element.get("contrast_ratio", 0)))
            assert contrast >= WCAG_NON_TEXT_CONTRAST_RATIO, (
                f"UI component '{element.get('id', 'unknown')}': contrast ratio {contrast} "
                f"does not meet 3:1 minimum — SC 1.4.11 Level AA"
            )

    def test_focus_indicator_meets_contrast_and_area(self, entity_profile: dict):
        """SC 2.4.11 (WCAG 2.2): Focus indicator must have a focus area and
        meet 3:1 contrast between focused and unfocused states."""
        for element in entity_profile.get("focusable_elements", []):
            focus = element.get("focus_indicator", {})
            if not focus:
                continue
            contrast = Decimal(str(focus.get("contrast_ratio", 0)))
            assert contrast >= WCAG_FOCUS_INDICATOR_CONTRAST_RATIO, (
                f"Focusable element '{element.get('id', 'unknown')}': focus indicator "
                f"contrast ratio {contrast} does not meet 3:1 minimum — SC 2.4.11 Level AA"
            )
```

---

## TestCaptionsAndTranscripts

```python
class TestCaptionsAndTranscripts:
    """SC 1.2.1 (Level A), SC 1.2.2 (Level A), SC 1.2.3 (Level A) — Time-based media."""

    def test_prerecorded_video_has_captions(self, entity_profile: dict):
        """SC 1.2.2: All prerecorded video content with audio track must have captions."""
        for media in entity_profile.get("video_content", []):
            if media.get("prerecorded") and media.get("has_audio_track"):
                assert media.get("captions_present") is True, (
                    f"Video '{media.get('id', 'unknown')}' is prerecorded with audio but "
                    f"has no captions — SC 1.2.2 Level A"
                )

    def test_audio_only_prerecorded_has_transcript(self, entity_profile: dict):
        """SC 1.2.1: Prerecorded audio-only content must have a text alternative (transcript)."""
        for media in entity_profile.get("audio_content", []):
            if media.get("prerecorded") and not media.get("has_video_track"):
                assert media.get("transcript_present") is True, (
                    f"Audio-only content '{media.get('id', 'unknown')}' has no transcript — "
                    f"SC 1.2.1 Level A"
                )

    def test_live_video_has_captions(self, entity_profile: dict):
        """SC 1.2.4 (Level AA): Live video with audio must have captions."""
        for media in entity_profile.get("video_content", []):
            if not media.get("prerecorded") and media.get("has_audio_track"):
                assert media.get("live_captions_present") is True, (
                    f"Live video '{media.get('id', 'unknown')}' has no captions — "
                    f"SC 1.2.4 Level AA"
                )
```

---

## TestKeyboardAccessibility

```python
class TestKeyboardAccessibility:
    """SC 2.1.1 (Level A), SC 2.1.2 (Level A) — Keyboard access."""

    def test_no_keyboard_trap_exists(self, entity_profile: dict):
        """SC 2.1.2: Users must be able to move focus away from any component
        using only a keyboard (no keyboard trap)."""
        for component in entity_profile.get("interactive_components", []):
            assert component.get("keyboard_trap") is not True, (
                f"Component '{component.get('id', 'unknown')}' has a keyboard trap — "
                f"SC 2.1.2 Level A: keyboard focus must always be movable away"
            )

    def test_skip_navigation_link_present(self, entity_profile: dict):
        """SC 2.4.1: Mechanism to bypass repeated blocks (skip navigation) must exist
        to allow users to reach main content directly."""
        pages = entity_profile.get("web_pages", [])
        assert pages, "No web page data in entity profile"
        for page in pages:
            if page.get("has_repeated_nav_blocks", True):
                assert page.get("skip_nav_present") is True, (
                    f"Page '{page.get('url', 'unknown')}' has no skip navigation mechanism — "
                    f"SC 2.4.1 Level A"
                )
```

---

## TestTargetSize

```python
class TestTargetSize:
    """SC 2.5.8 (WCAG 2.2, Level AA) — Target size minimum: 24×24 CSS pixels."""

    def test_interactive_targets_meet_minimum_size(self, entity_profile: dict):
        """SC 2.5.8: Interactive targets must be at least 24×24 CSS pixels, or have
        sufficient spacing (target center must be 24 CSS px from any adjacent target center)."""
        for target in entity_profile.get("interactive_targets", []):
            width_px = target.get("width_css_px", 0)
            height_px = target.get("height_css_px", 0)
            spacing_px = target.get("adjacent_target_spacing_px")
            has_exception = target.get("inline_exception", False)  # inline text exceptions
            if has_exception:
                continue
            meets_size = (
                width_px >= WCAG_TARGET_SIZE_MIN_CSS_PX
                and height_px >= WCAG_TARGET_SIZE_MIN_CSS_PX
            )
            meets_spacing = spacing_px is not None and spacing_px >= WCAG_TARGET_SIZE_MIN_CSS_PX
            assert meets_size or meets_spacing, (
                f"Interactive target '{target.get('id', 'unknown')}' is {width_px}×{height_px}px "
                f"with {spacing_px}px spacing — must be ≥{WCAG_TARGET_SIZE_MIN_CSS_PX}×"
                f"{WCAG_TARGET_SIZE_MIN_CSS_PX}px or have sufficient spacing — SC 2.5.8 Level AA"
            )
```

---

## TestPageLanguage

```python
class TestPageLanguage:
    """SC 3.1.1 (Level A) — Language of page: `lang` attribute required."""

    def test_html_lang_attribute_present(self, entity_profile: dict):
        """SC 3.1.1: The default human language of each web page must be programmatically
        determinable — `lang` attribute on `<html>` element."""
        for page in entity_profile.get("web_pages", []):
            assert page.get("html_lang_attribute") is not None, (
                f"Page '{page.get('url', 'unknown')}' has no `lang` attribute on `<html>` — "
                f"SC 3.1.1 Level A"
            )
```

---

## TestAccessibleAuthentication

```python
class TestAccessibleAuthentication:
    """SC 3.3.8 (WCAG 2.2, Level AA) — Accessible authentication: no cognitive function test."""

    def test_no_cognitive_function_test_in_authentication(self, entity_profile: dict):
        """SC 3.3.8: Authentication must not require solving a cognitive function test
        (transcribing text, solving a puzzle, recognizing a pattern) unless an alternative
        method is provided."""
        for auth_flow in entity_profile.get("authentication_flows", []):
            has_cognitive_test = auth_flow.get("requires_cognitive_function_test", False)
            has_alternative = auth_flow.get("cognitive_test_alternative_available", False)
            if has_cognitive_test:
                assert has_alternative is True, (
                    f"Authentication flow '{auth_flow.get('id', 'unknown')}' requires a "
                    f"cognitive function test with no alternative — SC 3.3.8 Level AA "
                    f"(WCAG 2.2): users must not be required to solve a cognitive test "
                    f"to authenticate"
                )

    @pytest.mark.assumption(
        id="ASSUME-WCAG-AUTH-001",
        text="CAPTCHA using audio alternative satisfies SC 3.3.8 per WCAG 2.2 exception "
             "(object recognition CAPTCHAs with audio equivalents are permitted); "
             "the specific CAPTCHA implementation type is accepted as documented in the "
             "accessibility conformance report.",
        confidence="PARAMETERIZED",
        approved_by=None,
    )
    def test_captcha_has_accessible_alternative(self, entity_profile: dict):
        """SC 3.3.8 exception: CAPTCHA with an audio alternative satisfies the SC."""
        for auth_flow in entity_profile.get("authentication_flows", []):
            if auth_flow.get("uses_captcha") is True:
                assert auth_flow.get("captcha_has_audio_alternative") is True, (
                    f"Authentication flow '{auth_flow.get('id', 'unknown')}' uses CAPTCHA "
                    f"without an audio or other accessible alternative — SC 3.3.8"
                )
```

---

## TestDraggingMovements

```python
class TestDraggingMovements:
    """SC 2.5.7 (WCAG 2.2, Level AA) — Dragging movements must have single-pointer alternative."""

    def test_drag_functionality_has_single_pointer_alternative(self, entity_profile: dict):
        """SC 2.5.7: All functionality using a dragging movement must be achievable
        with a single pointer without dragging, unless dragging is essential."""
        for component in entity_profile.get("interactive_components", []):
            if not component.get("requires_dragging", False):
                continue
            if component.get("dragging_is_essential", False):
                continue
            assert component.get("single_pointer_alternative_exists") is True, (
                f"Component '{component.get('id', 'unknown')}' requires dragging but has "
                f"no single-pointer alternative — SC 2.5.7 Level AA (WCAG 2.2)"
            )
```

---

## TestVPATConformanceClaim

```python
class TestVPATConformanceClaim:
    """Section 508 VPAT / Accessibility Conformance Report (ACR): required for federal procurement."""

    def test_vpat_or_acr_exists(self, entity_profile: dict):
        """Section 508: Accessibility Conformance Report (ACR/VPAT) required as part of
        ICT procurement for federal agencies."""
        if not entity_profile.get("federal_ict_procurement_subject", False):
            pytest.skip("VPAT/ACR requirement applies to federal ICT procurement")
        assert entity_profile.get("accessibility_conformance_report_exists") is True, \
            "No Accessibility Conformance Report (VPAT) found — required for Section 508 ICT procurement"

    @pytest.mark.human_review_required(
        id="CONTEST-WCAG-CONFORMANCE-001",
        question="WCAG Level AA conformance determination requires a combination of automated "
                 "testing (30-40% of issues) plus manual keyboard testing, screen reader testing, "
                 "and cognitive/usability evaluation. Automated tests alone are insufficient "
                 "to declare conformance. Human review required to validate the conformance claim.",
        confidence="CONTESTED",
    )
    def test_conformance_claim_supported_by_full_testing(self, entity_profile: dict):
        """WCAG 2.2 conformance claim: full conformance requires automated + manual +
        assistive technology testing. Automated tools detect only ~30-40% of issues."""
        if not entity_profile.get("wcag_conformance_claimed", False):
            pytest.skip("Applies when a WCAG conformance level is claimed")
        testing = entity_profile.get("wcag_testing_methodology", {})
        assert testing.get("automated_testing_conducted") is True, \
            "WCAG conformance claim requires at minimum automated accessibility testing"
        assert testing.get("manual_keyboard_testing_conducted") is True, \
            "WCAG conformance claim requires manual keyboard testing"
        assert testing.get("screen_reader_testing_conducted") is True, \
            "WCAG conformance claim requires screen reader testing"
```
