# KPI Versioning, Lineage & Retirement

`KPITarget` changes create `KPITargetVersion` records while preserving historical targets as immutable.

`KPIReplacement` tracks KPI retirement and replacement lineage (`old_kpi_id` -> `replaced_by_kpi_id`) for complete auditability.
