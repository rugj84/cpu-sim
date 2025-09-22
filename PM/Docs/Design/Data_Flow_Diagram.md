# CS104 CPU Simulator — Data Flow Diagram

[← Back to Project Management Index](../../README.md)

**Author:** Javier Ruiz Galan  
**Date:** September 2025  

---

## 1. Level 0 (Context Diagram)
At a glance, the **CPU Simulator** is a single system that:
- **Ingests** an instruction file and a data (memory) file,
- **Executes** instructions using a CPU + Cache + Memory Bus,
- **Emits** console logs/traces and final state.

```mermaid
graph TD
  %% External Entities
  U[User]
  IF[Instruction File]
  DF[Data File]
  CO[Console Output]

  %% System Boundary
  subgraph S[CPU Simulator]
    SB[System Core]
  end

  %% Flows
  U -->|Run config| S
  IF -->|Load instructions| S
  DF -->|Load data| S
  S -->|Logs results| CO
```

## 2. Level 1 




