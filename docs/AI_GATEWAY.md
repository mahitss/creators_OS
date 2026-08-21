# KINETIQ — AI Gateway & Model Routing Architecture

## 1. Gateway Overview

The KINETIQ AI Gateway serves as the centralized, fault-tolerant model routing layer connecting application services to OpenRouter and external LLM providers.

```
                  [KINETIQ AI GATEWAY]
                           |
             +-------------+-------------+
             |                           |
     [Model Policy Guard]        [Cost Governor & DLP]
             |                           |
             +-------------+-------------+
                           |
                     [Model Router]
                           |
        +------------------+------------------+
        |                  |                  |
   Fast Tier          Reasoning Tier      Fallback Tier
(gpt-4o-mini /       (deepseek-r1 /     (openrouter/free)
  llama-3.3-70b)       claude-3.5-sonnet)
```

---

## 2. Multi-Tier Fallback & Circuit Breakers

1. **Primary Route**: Requests are dispatched to the designated capability model (e.g. `meta-llama/llama-3.3-70b-instruct`).
2. **Model 404 / 503 Auto-Fallback**: If the target model returns 404 or fails connectivity, the gateway automatically falls back to `openrouter/free` without throwing unhandled 500s to the caller.
3. **Exponential Backoff**: Automatic retry with jitter on HTTP 429 rate limit responses.
4. **Token Accounting**: Every response records exact `prompt_tokens`, `completion_tokens`, and calculated USD cost attributed to the tenant.

---

## 3. Supported Execution Modes

- **Synchronous Generation (`generate`)**: Low-latency non-streaming completions.
- **Server-Sent Events (`stream`)**: Real-time token streaming over HTTP/2.
- **Structured Output (`structured_output`)**: Strict JSON schema enforcement with Pydantic validation.
