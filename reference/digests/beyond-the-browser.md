# beyond-the-browser — source digestion shell

Status: TRACK A COMPLETE (2026-08-22), 5 unique cited URLs reconciled per v1.7 currency conventions.
All five are official product/platform documentation (React Native, Electron, Samsung Tizen,
LG webOS, WeChat Mini Game) — authority anchors per house convention; fetch-on-demand. The
doc's mechanics sections are doc-native teaching grounded in those canon references.

## Cited-URL reconciliation (coverage gate requirement)

| cited URL | status | source-dated |
|---|---|---|
| https://reactnative.dev/architecture/landing-page | platform canon — RN New Architecture (JSI/Fabric/TurboModules) | continuously updated |
| https://www.electronjs.org/docs/latest/tutorial/process-model | platform canon — main/renderer/IPC process model | continuously updated |
| https://developer.samsung.com/smarttv/develop/getting-started/creating-tv-applications.html | platform canon — Tizen TV web apps + certification | continuously updated |
| https://webostv.developer.lge.com/ | platform canon — webOS TV web-app model, Enact, HLS | continuously updated |
| https://developers.weixin.qq.com/minigame/dev/guide/game-engine/engine-overview.html | platform canon — DOM-less mini-game sandbox, engine adapters | continuously updated |

No markup-artifact rows: no XML namespaces leaked into the citation set. No wikipedia,
papers, or standards bodies — this doc delegates entirely to vendor/platform canon.

## Coverage matrix

| doc section | covered by | note |
|---|---|---|
| #sec-how-to-use-this-doc | n/a navigation | exempt |
| #sec-definition-the-platform-bridge-problem | doc-native framing + cited canon (see ledger): rendering/security/distribution models, bridge vocabulary | eternal |
| #sec-the-outside-the-browser-map-what-javascript-runs-on | doc-native host map + owner-pointers (server/edge/embedded/AI owned by JavaScript Across Stacks) | eternal delegation structure; per-host facts live in owner docs |
| #sec-the-decision-matrix-when-to-use-what | doc-native decision table | R18 function · eternal defaults, surrounding landscape volatile→hedged |
| #sec-react-native-the-mobile-bridge | reactnative.dev New Architecture canon + doc-native walkthrough (transfer table, Expo vs bare, navigation) | eternal bridge→JSI shift; version milestones (0.76 default) dated-once · volatile→hedged |
| #sec-android-ios-platform-literacy-the-minimum-to-ship-and-debug | doc-native platform literacy (signing, permissions, review chains, crash reporting) | store-policy numbers drift → volatile→hedged |
| #sec-electron-tauri-the-desktop-bridge | electronjs.org Process Model canon + doc-native desktop comparison | eternal process/security model; bundle sizes volatile→hedged |
| #sec-pwa-and-capacitor-the-middle-ground | doc-native middle-ground comparison | eternal pattern ladder; capability limits volatile→hedged |
| #sec-smart-tv-tizen-webos-the-hidden-300m-screens | Samsung Tizen + LG webOS developer canon | continuously updated canon; fixed-Chromium model-year mapping dated-once · volatile→hedged |
| #sec-gaming-the-js-lane-outside-the-browser | WeChat Mini Game dev canon + doc-native lane table | eternal lane structure; 4MB package cap volatile→hedged |
| #sec-constraints-that-apply-to-every-installable-platform | doc-native cross-platform constraint matrix | eternal walls; store fees/policies volatile→hedged |
| #sec-the-native-landscape-link-don-t-duplicate | n/a shelf-internal — deliberate owner-pointer to JavaScript Across Stacks §4 | exempt |
| #sec-worked-example-a-habit-tracker-every-way | illustrative worked example (labeled), four bridges + one rejection | eternal illustration; Expo Router/file conventions volatile→hedged |
| #sec-most-common-failure-modes | traces to confirmed sections + cited canon rows | R15 support · eternal |
| #sec-principles | doc-native distilled defaults ("start with X unless Y") | eternal |
| #sec-summary-the-complete-mental-checklist | derives from confirmed sections | inherits classes |
| #sec-primary-sources | the citation ledger itself — mirrored in this shell's reconciliation table | inherits classes |
| #sec-ask-your-teacher | doc-native follow-up prompts; no new factual claims | eternal pedagogy |

## Gaps

| id | claim/area | hunts | status |
|---|---|---|---|
| G-bbtb1 | TV model-year→Chromium version mapping (2022≈94, 2025≈120, 2026≈126) | OEM firmware tables drift per model year; doc already hedges to feature-detect, never version-sniff | convention-tier hedge |
| G-bbtb2 | WeChat mini-game 4MB first-package cap + Cocos/Laya/Egret adapter matrix | Chinese-first, region-gated docs move fast; re-verify against engine changelogs | fetch next touch |
| G-bbtb3 | Store-review durations (Play "1–7 days", App Store "1–3 days") | policy numbers shift; doc frames them as release-planning guidance, not guarantees | convention-tier hedge |

## Content authored from this digestion

- Track B row: justified N/A this pass — rich authored doc delegating facts to cited
  canon (vendor/platform docs above); recorded per SHELF-DONE rule (additions OR
  justified N/A). HTML docs untouched.
