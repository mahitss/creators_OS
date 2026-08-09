# Vapor OS — Memory Provenance & Traceability

## 1. Traceable Memory Provenance
Every persistent memory retains explicit source references:
```json
{
  "memory_id": "mem_a1b2c3d4",
  "statement": "Project uses PostgreSQL 16",
  "scope": "workspace",
  "confidence": 1.0,
  "source_references": [
    {
      "type": "drive",
      "source_id": "doc_arch_spec_01",
      "title": "Architecture Specification v2",
      "location": "Section 4.1 Data Storage"
    }
  ],
  "approved_by": "usr_alex"
}
```

## 2. "Why does Vapor know this?"
Users can click **Provenance** in the UI to inspect the exact source document, paragraph location, confidence score, and approving user. Vapor never uses generic "AI generated" as sole provenance for important facts.
