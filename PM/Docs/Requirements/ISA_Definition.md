# ISA Definition

[← Back to Index](../../README.md)  

**Author:** Javier Ruiz Galan  
**Date:** September 2025  

---

## 1. Supported Instructions
- **ADD** – `Rd <- Rs + Rt`
- **ADDI** – `Rt <- Rs + immediate`
- **SUB** – `Rd <- Rs - Rt`
- **SLT** – `Rd <- (Rs < Rt) ? 1 : 0`
- **BNE** – `if (Rs != Rt) PC <- (PC + 4) + offset * 4`
- **J** – `PC <- target * 4`
- **JAL** – `R7 <- PC + 4; PC <- target * 4`
- **LW** – `Rt <- MEM[Rs + offset]`
- **SW** – `MEM[Rs + offset] <- Rt`
- **CACHE** – `0 (off), 1 (on), 2 (flush)`
- **HALT** – Terminate execution

---

## 2. Instruction Formats
- **R-Type** (Register):  
  `[OPCODE][Rs][Rt][Rd][shamt][funct]`

- **I-Type** (Immediate):  
  `[OPCODE][Rs][Rt][Immediate]`

- **J-Type** (Jump):  
  `[OPCODE][Target]`

---

## 3. Encoding Examples
Examples based on simplified binary/hex encoding:

- **ADD R3, R2, R1**  
  R-Type: `000000 00010 00001 00011 00000 100000`

- **ADDI R2, R2, 2**  
  I-Type: `001000 00010 00010 0000 0000 0000 0010`

- **J 8**  
  J-Type: `000010 0000 0000 0000 0000 0000 1000`

- **CACHE 1**  
  I-Type (custom): `111111 00000 00000 00000 0000 0000 0001`

- **HALT**  
  Special: `111110 00000 00000 00000 00000 000000`

---
