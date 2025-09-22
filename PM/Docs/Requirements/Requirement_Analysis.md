# CS104 CPU Simulator — Requirement Analysis

[← Back to Project Management Index](../../README.md)

**Author:** Javier Ruiz Galan  
**Date:** September 2025  

---

## 1. Introduction

### Project Overview
This project aims to design and implement a Python-based CPU simulator that models the internal operations of a simplified CPU, its cache, and memory bus. The simulator will read instructions from an input file and initial memory values from another input file, then execute the instructions step by step according to a custom Instruction Set Architecture (ISA) inspired by MIPS.

### Objectives
- Develop a Python program that simulates a CPU, cache, and memory bus.
- Implement a simplified MIPS-like ISA supporting arithmetic, branching, memory operations, and cache control.
- Parse and process initialization data and instructions from external input files.
- Provide console outputs documenting execution stages for transparency and debugging.

### Scope
The simulator will focus on simulating the **fetch-decode-execute cycle**, interaction with a **memory bus**, and **cache control**.  
It will not model micro-architecture details like pipelines, hazards, or speculative execution.  

---

## 2. Functional Requirements

### Instruction Set Architecture (ISA)
The simulator must implement the following instructions:

- **Arithmetic/Logic:**  
  - `ADD Rd, Rs, Rt` → `Rd <- Rs + Rt`  
  - `ADDI Rt, Rs, imm` → `Rt <- Rs + imm`  
  - `SUB Rd, Rs, Rt` → `Rd <- Rs - Rt`  
  - `SLT Rd, Rs, Rt` → `if (Rs < Rt) Rd <- 1 else Rd <- 0`  

- **Control Flow:**  
  - `BNE Rs, Rt, offset` → if `(Rs != Rt)` then `PC <- (PC + 4) + offset * 4`  
  - `J target` → `PC <- target * 4`  
  - `JAL target` → `R7 <- PC + 4; PC <- target * 4`  

- **Memory:**  
  - `LW Rt, offset(Rs)` → `Rt <- MEM[Rs + offset]`  
  - `SW Rt, offset(Rs)` → `MEM[Rs + offset] <- Rt`  

- **Cache Control:**  
  - `CACHE code` →  
    - `0` → Cache off  
    - `1` → Cache on  
    - `2` → Flush cache  

- **System:**  
  - `HALT` → Terminate execution  

### Inputs/Outputs
- **Inputs:**  
  - `instruction_input.txt`: Contains instructions in the format `<INSTRUCTION>,<ARG1>,...,<ARGn>`  
    Example:  
    ```
    CACHE,1
    ADDI,R2,R2,2
    ADD,R3,R2,R1
    J,8
    HALT,;
    ```
  - `data_input.txt`: Contains initial memory address-value pairs `<ADDRESS>,<VALUE>`  
    Example:  
    ```
    00000001,4
    00000010,5
    00000011,6
    ```

- **Outputs:**  
  - Console logs documenting:  
    - Instruction fetch, decode, and execution  
    - Register updates  
    - Memory/cache operations  
  - Final state of registers and memory after execution halts  

### Expected Behavior
- The CPU fetches instructions sequentially unless a branch/jump modifies the PC.  
- Instructions update registers or memory based on their operation.  
- Cache instructions modify cache behavior (on/off/flush).  
- Execution terminates when `HALT` is encountered.  

---

## 3. Non-Functional Requirements

### Performance
- Should handle instruction sequences of at least several hundred lines with minimal delay.  
- Cache operations should reduce memory access times when enabled.  

### Reliability
- Must correctly parse valid input files and gracefully handle invalid instructions or malformed data.  
- Execution must stop safely upon encountering `HALT`.  

### Usability
- Console outputs must be human-readable, clearly showing each stage of execution.  
- Easy modification of ISA or input files for testing purposes.  

---

## 4. Constraints

### Tools & Languages
- **Programming Language:** Python 3.13  
- **Editor:** VS Code  
- **Version Control:** GitHub for repository and commits  

### Hardware/Software Limitations
- Runs on standard desktop environments (Windows/Mac/Linux).  
- Memory bus simulation limited to integer values.  
- No GUI, only console-based output.  

---

## 5. Assumptions
- Instruction and data input files are correctly formatted.  
- Memory addresses are unique and valid.  
- Registers are initialized to `0` unless specified by execution.  
- Cache simulation is simplified (enable/disable/flush) without modeling replacement policies.  
- PC (program counter) starts at the first instruction (address 0).  

---
