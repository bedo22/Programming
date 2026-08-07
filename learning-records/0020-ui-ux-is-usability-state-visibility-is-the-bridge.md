# 0020 — The human layer: UI/UX is usability, and state visibility is the bridge

**Date:** 2026-08-06
**Lesson:** `lessons/0020-the-human-layer.html`
**Reference:** `reference/ui-ux-web-design.html` §1, §8, §9

## Context
The Human/product movement begins. This lesson turns the whole journey one layer outward: 19 lessons covered the engine (language, platform, state, rhythm, system, process); this covers the interface people actually touch. The learner's mission is conceptual literacy in the frontend ecosystem — and UI/UX is a first-class layer of that ecosystem, not "making it pretty."

## Key insight
UI/UX is **four disciplines** (Interaction Design, Visual/UI, UX research, UX/web design) targeting **usability** — least friction to the goal — not decoration. For a developer, the single most valuable insight is **state visibility**: every UI state (loading, empty, error, success, disabled) must be visibly distinct, and this maps directly onto the state modeling from L3. The most common UI bug is a table showing "empty" while still loading — that's a *state modeling* failure, not a styling failure. Accessibility (WCAG AA) is now a legal baseline that improves usability for everyone (curb-cut effect).

## Why this matters for future sessions
This directly connects the whole map backward: state visibility (L3 state), the DOM/accessibility tree (L2 platform), semantic HTML (L2), and the rhythm (L7) all show up as the *implementation* of UI/UX decisions. It gives the learner a concrete, code-level handle on an otherwise "soft" discipline. Next: L21 (Design Thinking) is the layer upstream that decides *what* to build, and L22 (Income/Markets) closes the Human/product movement.
