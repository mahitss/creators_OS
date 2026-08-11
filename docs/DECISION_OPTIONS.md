# Decision Options & Trade-Off Matrix

Details option generation, criteria evaluation, and trade-off matrices in Vapor OS.

## Option Evaluation
- Options are evaluated against weighted criteria (`cost`, `latency`, `reliability`, `security`, `quality`, `time`, `compliance`).
- Side-by-side trade-off comparisons (`DecisionTradeoff`) explicitly detail advantages and disadvantages of competing options.
- If evidence is insufficient to distinguish options, the engine returns `insufficient_information`.
