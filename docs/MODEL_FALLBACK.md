# Bounded Policy-Compliant Fallbacks

When a primary model provider experiences timeouts, rate limits, or degradation, Model Gateway executes bounded fallback routing.

## Fallback Rules
1. **Independent Policy Verification**: Fallback models MUST independently pass capability, policy, and DLP checks.
2. **No Blind Fallback**: Never fallback to arbitrary or unauthorized providers.
3. **Bounded Attempts**: Maximum fallback attempts are strictly bounded (default max 2 retries).
4. **Audit Recording**: Records original model, fallback model, and degradation reason in `ModelRoutingDecision`.
