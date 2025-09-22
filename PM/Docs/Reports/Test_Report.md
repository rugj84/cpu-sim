# CS104 CPU Simulator — Test Report

[← Back to Project Management Index](../../README.md)

**Author:** Javier Ruiz Galan  
**Date:** September 2025  

---

## 1. Test Plan

### Test Objectives
- Verify that the CPU Simulator correctly executes supported MIPS-like instructions (ADD, ADDI, SUB, SLT, BNE, J, JAL, LW, SW, CACHE, HALT).  
- Validate initialization and data loading of the Memory Bus from `data_input.txt`.  
- Confirm correct parsing of instructions from `instruction_input.txt`.  
- Ensure CPU, Cache, and Memory Bus interactions behave as expected.  
- Check console output and program termination behavior.

### Scope
- Unit tests for CPU initialization and instruction execution.  
- Integration tests for CPU, Cache, and Memory Bus interactions.  
- Parsing tests for instruction and data input files.  
- Smoke test for the main program entry point.  

---

## 2. Test Cases

| **Test Case**              | **Input** | **Expected Output** | **Actual Result** | **Status** |
|-----------------------------|-----------|---------------------|-------------------|-------------|
| CPU Initialization          | No input (object creation) | CPU registers = 0, PC = 0 | Matches expected | ✅ PASSED |
| ADDI + ADD Execution        | Instructions: `ADDI R2,R2,2; ADD R3,R2,R1` | Correct arithmetic update in registers | Matches expected | ✅ PASSED |
| Branch and Jump Flow        | Instruction sequence with `BNE` + `J` | Correct PC updates (branch/jump) | Matches expected | ✅ PASSED |
| Cache Writeback + Flush     | Instruction `CACHE,2` | Cache flushed successfully | Matches expected | ✅ PASSED |
| Main Program Smoke Test     | `instruction_input.txt` + `data_input.txt` | Program executes until HALT | Matches expected | ✅ PASSED |
| Program Parsing             | `instruction_input.txt` | Parsed into internal representation | Matches expected | ✅ PASSED |
| Memory Bus Load + RW        | `data_input.txt` | Values correctly loaded and accessible | Matches expected | ✅ PASSED |

---

## 3. Bug Tracking

### Current Results
- **All 7 tests passed.**  
- **Coverage:** 68% overall.  
  - `cache.py`: 70% (missing edge cases in eviction/write-back).  
  - `cpu.py`: 75% (missing untested ISA branches and error handling).  
  - `main.py`: 0% (no tests directly invoking CLI/entrypoint).  
  - `memory_bus.py`: 96% (one branch uncovered).  

### Open Issues
- **Low coverage in `main.py` (0%)**: Add functional/system-level tests that run the simulator end-to-end.  
- **Uncovered code paths in `cpu.py`**: Add tests for edge ISA cases (`SLT`, `SW`, `LW`, error conditions).  
- **Cache edge cases**: Expand tests for cache misses, multiple evictions, and disabled cache mode.  

---

✅ **Conclusion:** The CPU Simulator passes all implemented tests and demonstrates functional correctness for core ISA instructions and components. Further work is needed to expand test coverage (especially `main.py` and uncovered CPU/cache logic).  

