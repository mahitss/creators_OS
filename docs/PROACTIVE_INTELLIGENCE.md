# Proactive Intelligence & Truthful Insights

## Critical Principle
Vapor OS distinguishes **Events** from **Signals**, **Insights**, and **Actions**:
- **Events**: Raw environment occurrences (e.g. 100 emails received).
- **Signals**: Meaningful changes filtered deterministically (e.g. 1 email from a key client regarding project timelines).
- **Insights**: Executive high-signal summaries stating facts truthfully (e.g. "Potential schedule conflict detected with client review").
- **Actions**: Gated proposals (Attention item, Approval request, or Policy-evaluated Agent run).

## Truthful Insight Generation
The system adheres to strict truthfulness rules:
- No fabricated claims: If evidence confirms a schedule overlap, the title states "Potential Schedule Conflict Detected" rather than asserting absolute certainty without complete calendar availability.
- Source references: Every Insight retains links to underlying `source_events` and `source_references`.

## Attention Center Integration
Insights are seamlessly integrated into the existing Attention Center (`/attention`) without creating separate notification noise. Users can dismiss insights or act upon them.
