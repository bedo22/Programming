# 0008 — Angular: three eras, same direction, different mechanism than React

- **Date:** 2026-07-30
- **Episode:** 8 (The Other Path)
- **Status:** Active

## Context
Lesson 8 contrasted Angular with React. The trap it dissolves: assuming every framework took React's path, then misreading Angular code by forcing React's model onto it.

## The insight
Angular is **three frameworks with one name**, each rewriting reactivity from scratch: AngularJS (2010–2016, dirty-checking over a `$scope` tree), Angular 2+ (2016–2023, classes + TypeScript + DI + zone.js broadcasting to all components), and Modern Angular (2023+, Signals + standalone + zoneless, a fine-grained subscription graph). The direction is the same as React's — **narrow what the framework watches** — but the mechanism differs: React narrowed the *component's* awareness of what changed (`this.setState` → deps arrays → compiler inference); Angular narrowed the *framework's* watching (`$scope` tree → all components → signal graph). That's also why Angular adopted Signals while React declined: different bottlenecks — Angular's was zone.js's broadcast (Signals fix it), React's was the manual deps-array tax (the compiler fixes it without breaking the per-render capture model Signals would break).

## Why it matters
This lets the learner place Angular code at work (enterprise/government niches) without converting it to React's model — and it sharpens the React mental model by contrast. The "same direction, different mechanism" pattern generalizes: frameworks converge on narrower reactivity but diverge on how. Feeds Episode 9 (the compiler is React's answer where Signals were Angular's).

## Evidence
- `reference/angular-evolution.html` §0 (the three-era table), §2.9 (hooks-Signals contrast), the Q&A win section.
- `lessons/0008-the-other-path.html`.

## Revisions
_(none yet)_
