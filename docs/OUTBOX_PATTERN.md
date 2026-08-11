# Transactional Outbox Pattern

## Database-to-Event Atomicity
To avoid dual-write inconsistencies between database transactions and event publishing, Vapor OS implements the Transactional Outbox Pattern (`EventOutbox`):

1. State changes and event envelopes are written to the database in a single atomic transaction.
2. The Outbox Publisher processes pending records and dispatches them to the Event Router.
3. Outbox status transitions from `pending` to `published` upon confirmation.
