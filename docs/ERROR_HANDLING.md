# Vapor OS — Application Error Handling & Taxonomy

## 1. Error Taxonomy
All application errors are categorized using standardized error codes:
- `AUTHENTICATION_ERROR`
- `AUTHORIZATION_ERROR`
- `VALIDATION_ERROR`
- `NOT_FOUND`
- `CONFLICT`
- `RATE_LIMITED`
- `DATABASE_ERROR`
- `AI_PROVIDER_ERROR`
- `AI_VALIDATION_ERROR`
- `WORKER_ERROR`
- `EXTERNAL_SERVICE_ERROR`
- `INTERNAL_ERROR`

## 2. Standardized Error Response Format
All HTTP error responses return a uniform JSON body:
```json
{
  "error_code": "NOT_FOUND",
  "message": "The requested resource could not be found.",
  "request_id": "req-uuid-1234",
  "path": "/api/v1/missions/mis-999",
  "details": {}
}
```
