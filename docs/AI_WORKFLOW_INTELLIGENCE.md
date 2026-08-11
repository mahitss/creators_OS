# AI Workflow Intelligence Architecture

## Overview
Vapor OS AI Workflow Intelligence serves as an authoring assistant layer built on top of the visual workflow engine, policy engine, and DAG runtime.

## Core Architectural Pipeline
```
USER PROMPT
   ↓
AI WORKFLOW COPILOT
   ↓
PROMPT SANITIZATION & INJECTION DEFENSE
   ↓
STRUCTURED PROPOSAL GENERATION
   ↓
SCHEMA & KAHN CYCLE VALIDATION
   ↓
POLICY ENGINE CAPABILITY REVIEW & DETERMINISTIC RISK CLASSIFICATION
   ↓
HUMAN REVIEW & VISUAL DIFF
   ↓
ACCEPT PROPOSAL (Creates Draft Version)
   ↓
MANUAL PUBLISH
   ↓
AUTHORITATIVE DAG ENGINE
```

## Critical Guarantees
- **AI is an Authoring Assistant, NOT the Runtime**: AI generates proposals, explanations, diagnostics, and optimizations. It NEVER mutates active workflows or executes production nodes directly.
- **No Direct Mutation or Auto-Publishing**: Accepting an AI proposal creates a draft `WorkflowVersion`. Publishing requires manual human review and policy validation.
- **Dynamic Code Execution Forbidden**: AI proposals cannot contain Python, JavaScript, Shell, or SQL code execution nodes.
