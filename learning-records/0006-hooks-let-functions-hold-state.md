# 0006 — Hooks let functions hold state; classes aren't gone, just legacy

- **Date:** 2026-07-30
- **Episode:** 6 (The Class→Hooks Revolution)
- **Status:** Active

## Context
Lesson 6 closed the Ecosystem movement. The trap it dissolves: thinking "functional programming" alone drove React's move from classes — when the real reason is that functions couldn't hold state *until hooks gave them the power*.

## The insight
React 2013–2018 used **class components** (`this.state`, `bind`, lifecycle methods). The React team named three pains over five years of maintaining tens of thousands of components: (1) hard to reuse stateful logic → "wrapper hell" of HOCs/render props; (2) giant components with one concern scattered across many lifecycle methods; (3) `this` confusion (officially, "Introducing Hooks," 2018). The counterintuitive key: **function components already existed before hooks — they were just stateless and effect-less**, so they couldn't replace classes for real work. Hooks (2018) gave functions `useState` (state) and `useEffect` (side effects), which is what made functions viable. Deeper still: functions **capture** rendered values (closures, correct by default); `this` **mutates** (buggy). And per Lesson 3, state just moved from the class instance to a **React-owned hook slot** — same variable, different owner. Classes remain in the spec under "Legacy API," but are no longer taught first.

## Why it matters
This is the internal story behind every modern React codebase the learner will read. It also sets up Episode 9 (the React Compiler removes the last hooks-era friction — manual memoization) and ties back to Episode 3 (state's "where does it live" across eras). The "capture vs mutate" insight is the bridge to reading effects and stale-closure behavior confidently.

## Evidence
- `reference/class-to-hooks-paradigm-shift.html` §6 (the three problems + hooks), the deeper-reason callout (capture vs mutate), §15–16.
- `lessons/0006-the-class-to-hooks-revolution.html`.
- React, "Introducing Hooks" (legacy.reactjs.org/docs/hooks-intro.html, 2018) — the three problems.

## Revisions
_(none yet)_
