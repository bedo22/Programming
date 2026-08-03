# 0009 — The compiler auto-memoizes; RSC splits the process; frameworks are the default

- **Date:** 2026-07-30
- **Episode:** 9 (The Frontier)
- **Status:** Active

## Context
Lesson 9 closed the Practice movement and the React story. The trap it dissolves: assuming the function+hooks model from 2018 is the end of the story, then being surprised by `"use client"`, the compiler, and the "use a framework" guidance.

## The insight
After hooks settled, React moved up-stack. (1) The **React Compiler v1.0** (Oct 2025) analyzes code and inserts memoization automatically — even where `useMemo` can't legally go — so `useMemo`/`useCallback`/`React.memo` become escape hatches, not the default; you write the simple version, the compiler puts the optimization back. (2) **React Server Components** split rendering across two computers: server components run once on the server (data, no hooks, no events), client components run in the browser with the full hooks model; `"use client"` marks the boundary. (3) **Create React App was sunset (Feb 2025)** — new apps should use a framework (Next.js, React Router framework mode, or Expo); Next.js is React + routing + server/client split + caching + tooling, and its App Router defaults to Server Components. Critically, the Lesson 6 model still holds — the compiler and RSC are layers on top, not replacements; client components still capture values per render.

## Why it matters
This is the landscape the learner will actually read at work in 2026. It also closes the React arc begun in Lesson 6 (classes → functions+hooks → functions+hooks+compiler+split-process) and motivates the System movement: once rendering splits across computers, the contract between them (Episode 10, API design) becomes first-class.

## Evidence
- `reference/react-2024-and-beyond.html` §1 (compiler), §2 (RSC), §7 (19.2 + CRA sunset).
- `reference/nextjs-deep-dive.html` §1–2 (what Next is, App vs Pages Router), §11 (work checklist).
- `lessons/0009-the-frontier.html`.

## Revisions
_(none yet)_
