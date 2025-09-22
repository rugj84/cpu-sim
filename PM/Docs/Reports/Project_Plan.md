# CS104 CPU Simulator — Project Plan

[← Back to Project Management Index](../../README.md)

**Author:** Javier Ruiz Galan  
**Date:** September 2025  

---

## 1. Objectives
- Design and implement a Python program simulating a simplified CPU.
- Support instruction fetch, decode, execute, memory access, and write-back.
- Implement a small ISA (MIPS subset: ADD, ADDI, SUB, SLT, BNE, J, JAL, LW, SW, CACHE, HALT).
- Load instructions from `instruction_input.txt` and memory initialization values from `data_input.txt`.
- Provide console logs to trace instruction execution and memory/cache behavior.

---

## 2. Scope
- **Included:**
  - CPU core (registers, PC, instruction decode/execute).
  - Memory Bus with initialized addresses/values.
  - Cache simulation (on/off/flush).
  - Instruction parsing from input file.
  - Console output of execution trace.
- **Excluded:**
  - GUI or visualization layer.
  - Multi-core CPU simulation.
  - Advanced pipeline hazards or branch prediction.

---

## 3. Deliverables
- **Python Source Code:**
  - `cpu.py` — CPU class.
  - `cache.py` — Cache class.
  - `memory_bus.py` — Memory bus class.
  - `main.py` — Entry point for simulator.
- **Input Files:**
  - `instruction_input.txt`
  - `data_input.txt`
- **Documentation:**
  - `README.md` with usage instructions.
  - Project management docs (Requirements, System Architecture, ISA Definition, Use Cases, Class Diagrams).
- **Execution Trace Output:**
  - Console logs showing instruction flow and memory/cache changes.

---

## 4. Timeline (1 Day)
| Time (hrs) | Task |
|------------|------|
| 0–2 | Set up project structure (VS Code, GitHub repo, folders for `src/`, `Docs/`, `PM/`). |
| 2–5 | Implement `MemoryBus` (load from file) and `Cache` class. |
| 5–8 | Implement `CPU` class with instruction fetch, decode, execute. |
| 8–10 | Integrate instruction + data loading, execution loop, HALT handling. |
| 10–12 | Testing using provided input files (`instruction_input.txt`, `data_input.txt`). |
| 12–14 | Debug & refine (cache behavior, jumps, edge cases). |
| 14–16 | Write documentation (README, project docs, diagrams). |
| 16–20 | Final testing & polish logs. |
| 20–24 | Buffer for risks, validation, GitHub commit & push. |

---

## 5. Risks & Mitigation
- **Risk:** Instruction parsing errors.  
  *Mitigation:* Implement strict parsing with error messages and fallback handling.  
- **Risk:** Incorrect ISA execution semantics.  
  *Mitigation:* Validate each instruction with small test cases.  
- **Risk:** Cache logic bugs (on/off/flush not working).  
  *Mitigation:* Unit tests for cache state changes.  
- **Risk:** Time overrun.  
  *Mitigation:* Prioritize CPU + Memory Bus core functionality first, cache second, extra docs last.  

