# KPI Measurements & Provenance Tracking

`KPIMeasurement` tracks actual values, timestamps, period boundaries, source names, and quality flags (`verified`, `estimated`, `partial`, `stale`, `missing`, `invalid`).

If data is missing or uncertain, it is marked `missing` or `estimated` without manufacturing values.
