# Enterprise Transformation Resilience Drift

## Dynamic Baselines & Drift Detection

Vapor compares normalized signals against dynamic, versioned resilience baselines to detect degradation.

## Drift Types
* **Temporary Anomaly**: Short-term transient noise that resolves automatically.
* **Persistent Drift**: Sustained deviation across consecutive observation windows.
* **Structural Drift**: Fundamental shift in underlying architecture or resource capacity.
* **Unknown Drift**: Unclassified deviation requiring investigation.
