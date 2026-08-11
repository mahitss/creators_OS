# Bounded Agent Delegation & Security Tokens

## Delegation Authority Rules
Parent agents delegate strictly within their own authority boundaries. Bounded security tokens (`DelegationContextToken`) specify parent, child, mission, task, scope, expiration, and policy version. Maximum delegation depth (default: 3) and cycle detection (`A -> B -> C -> A`) halt invalid circular delegation chains.
