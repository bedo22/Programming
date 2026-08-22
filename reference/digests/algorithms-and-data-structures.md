# algorithms-and-data-structures — source digestion shell

Status: TRACK A COMPLETE (2026-08-22). Five unique cited URLs reconciled per v1.7
currency conventions — one academic textbook companion (Kleinberg & Tardos), one
publisher book page (Zingaro), one practitioner lookup reference (Big-O Cheat Sheet),
one practice platform (HackerRank), one platform-canon page (MDN Map/Set). Authority
anchors per house convention; fetch-on-demand. Everything else in the doc is
doc-native teaching: settled algorithm/data-structure knowledge that needs no live
source, with code templates delegating language semantics to MDN.

## Cited-URL reconciliation (coverage gate requirement)

| cited URL | status | source-dated |
|---|---|---|
| https://www.cs.cornell.edu/home/kleinber/tgps/algorithm-design.html | textbook canon — Kleinberg & Tardos, *Algorithm Design* companion (the trade-off framework) | dated-once · eternal for settled theory |
| https://www.manning.com/books/algorithmic-thinking | practitioner canon — publisher page for Zingaro, *Algorithmic Thinking* (working templates, not theory) | dated-once per edition · catalog page living |
| https://bigocheatsheet.com/ | practitioner canon — Big-O Cheat Sheet, the lookup table behind §1 | continuously updated |
| https://www.hackerrank.com/ | practitioner platform — the interview screen this doc trains for | continuously updated |
| https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map | platform canon — MDN Map/Set real-key semantics backing §2 and the JS-cost table | continuously updated |

No XML-namespace/markup-artifact URLs found; all five are genuine sources.

## Coverage matrix

| doc section | covered by | note |
|---|---|---|
| #sec-how-to-use-this-doc | n/a navigation | exempt |
| #sec-complexity-the-quick-review | doc-native Big-O review + bigocheatsheet.com canon (see ledger); JS-operation cost table hedges engine drift | eternal classes · JS ops volatile→hedged |
| #sec-paradigm-selection-the-thinking-that-reaches-for-the-toolkit | doc-native six-paradigm framework + Kleinberg & Tardos trade-off canon (see ledger); signal table | authored framework · eternal · R18 function |
| #sec-arrays-strings-and-hashing-the-80 | doc-native templates (two pointers, sliding window, prefix sums) + MDN Map/Set canon (see ledger) | eternal |
| #sec-stacks-queues-and-linked-lists-the-shapes | doc-native templates incl. LRU-cache worked example (labeled illustrative) | eternal |
| #sec-trees-and-heaps-the-hierarchies | doc-native traversal/BST/trie/heap templates | eternal |
| #sec-recursion-the-self-referential-move | doc-native; D&C-vs-DP overlapping/independent subproblems distinction | eternal |
| #sec-graphs-the-model-of-connections | doc-native BFS/DFS/topological-sort/Dijkstra/Union-Find templates — settled algorithm canon | eternal |
| #sec-sorting-and-searching-the-preprocessing-moves | doc-native sort menu + binary-search half-open-range template; ES2019 stability note hedged | eternal core · engine notes dated-once |
| #sec-dynamic-programming-the-state-machine-of-optimization | doc-native state/transition/base teaching, memoize-before-tabulate order | eternal |
| #sec-greedy-the-beautiful-lie | doc-native exchange-argument test; unproven greedy handled as failure mode | eternal |
| #sec-bit-manipulation-and-math-the-trick-drawer | doc-native XOR identities, masks, Euclid/sieve staples | eternal |
| #sec-pattern-recognition-cheat-sheet-signal-technique | doc-native signal→technique decision table, operational twin of Problem-Solving's recognition tables | authored framework · eternal · R18 function |
| #sec-summary-the-complete-mental-checklist | derives from confirmed sections above | inherits classes · R20 checklist |
| #sec-failure-modes-the-edge-case-checklist | doc-native symptom→cause→fix rows tracing back to confirmed template sections | R15 support · eternal |

## Gaps

| id | claim/area | hunts | status |
|---|---|---|---|
| G-big1 | Hardware-level cost nuance (cache locality, branch prediction) behind why O() constants differ | deliberately delegated to CS & Software Engineering by the shelf split (proof side vs toolkit side) | convention-tier hedge |
| G-amt1 | Formal amortized-analysis proofs (banker/potential method) behind the "O(1) amortized" claims | doc teaches the working intuition only; textbook rigor left to cited Kleinberg & Tardos canon | accepted authored scope — toolkit, not textbook |

## Content authored from this digestion

- Track B row: justified N/A this pass — rich authored doc delegating facts to cited
  canon (Kleinberg & Tardos, Zingaro, Big-O Cheat Sheet, HackerRank, MDN); recorded
  per SHELF-DONE rule (additions OR justified N/A). Do NOT edit the HTML docs.
