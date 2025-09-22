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

## 2. Level 1 (Detailed Process Flow)

graph TD
  %% External Entities
  U[User]
  IF[Instruction File]
  DF[Data File]
  CO[Console Output]

  %% System Boundary
  subgraph SIM[CPU Simulator]
    %% Processes
    P0(Loader)
    P1(Fetch)
    P2(Decode)
    P3(Execute ALU)
    P4(Memory Access)
    P5(Write Back)
    P6(Cache Controller)
    P7(Program Control)

    %% Data Stores
    D1[(Instruction Store)]
    D2[(Register File)]
    D3[(Cache)]
    D4[(Memory Bus)]
    D5[(Trace Logger)]
  end

  %% Initialization
  IF -->|Instructions| P0
  DF -->|Address Value pairs| P0
  U  -->|Run config| P0

  P0 -->|Parsed instructions| D1
  P0 -->|Preload memory| D4
  P0 -->|Startup log| D5

  %% Pipeline
  P7 -->|PC| P1
  P1 -->|Instr| P2
  P2 -->|Control signals operands| P3
  P3 -->|ALU result branch info| P4
  P3 -->|Write back data R type| P5
  P4 -->|Load data LW| P5
  P5 -->|Updated regs| D2

  %% Operand sourcing
  D2 -->|Rs Rt values| P2
  P5 -->|Reg write| D2

  %% Memory Cache path
  P4 -->|Read Write req| P6
  P6 -->|Hit serve commit| D3
  P6 -->|Miss or flush| D4
  D3 -->|Data on hit| P4
  D4 -->|Data on miss| P4

  %% Control flow updates
  P2 -->|Branch jump signals| P7
  P3 -->|Branch taken| P7

  %% Logging
  P0 --> D5
  P1 --> D5
  P2 --> D5
  P3 --> D5
  P4 --> D5
  P5 --> D5
  P6 --> D5
  P7 --> D5

  D5 -->|Emit| CO

  %% Termination
  P2 -->|HALT detected| P7
  P7 -->|Stop signal| CO

## 3. Notations
- External Entities (square): Sources/sinks outside the system (User, files, console).
- Processes (rounded): Transformations on data (Loader, Fetch, Decode, Execute, Mem, WB, Cache Ctrl, PC/Flow).
- Data Stores (double-bracket): Persistent data inside the system (Instruction Store, Register File, Cache, Memory Bus, Trace/Logger).
- Data Flows (arrows): Movement of data between entities, processes, and stores.
