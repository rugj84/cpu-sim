# 🖥️ CS104 CPU Simulator

[![CI](https://github.com/rugj84/cpu-sim/actions/workflows/ci.yml/badge.svg)](https://github.com/rugj84/cpu-sim/actions/workflows/ci.yml)
[![Coverage](https://img.shields.io/codecov/c/github/rugj84/cpu-sim)](https://app.codecov.io/gh/rugj84/cpu-sim)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.12%20%7C%203.13-blue)](pyproject.toml)

A Python-based simulator that models a simplified CPU, memory bus, and cache.  
Implements a subset of **MIPS-like ISA**:

```
ADD, ADDI, SUB, SLT, BNE, J, JAL, LW, SW, CACHE, HALT
```

Designed for learning **computer architecture** and practicing **system-level Python design**.

---

## 🚀 Quickstart

### Requirements
- Python **3.12+**
- [uv](https://github.com/astral-sh/uv) or pip

### Install
```bash
# clone the repo
git clone https://github.com/rugj84/cpu-sim.git
cd cpu-sim

# create virtualenv + install deps with uv
uv sync --all-extras

# or with pip
pip install -e .
```

### Run Simulator
```bash
# using provided examples
python -m cpu_sim   --program examples/instruction_input.txt   --data examples/data_input.txt   --trace
```

---

## 📝 Example

### Example Input

**examples/instruction_input.txt**
```txt
CACHE,1
ADDI,R2,R2,2
ADD,R3,R2,R1
J,8
HALT,;
```

**examples/data_input.txt**
```txt
00000001,4
00000010,5
00000011,6
00000100,7
00000101,2
00000110,3
00000111,9
```

### Example Output (truncated)

```txt
[CPU] CACHE ON
[CPU] Fetch: ADDI R2, R2, 2
[CPU] Decode: Rs=R2=0, Rt=R2, imm=2
[CPU] Execute: R2 <- 0 + 2 = 2
[CPU] WriteBack: R2=2

[CPU] Fetch: ADD R3, R2, R1
[CPU] Execute: R3 <- 2 + 0 = 2
[CPU] WriteBack: R3=2

[CPU] Jump -> PC=8
[CPU] HALT
```

---

## 🧩 Features
- Instruction parsing from `.txt` files
- CPU with registers, PC, and control flow
- Memory Bus with initial data load
- Cache operations (off / on / flush)
- Pipeline trace output for debugging

---

## 📂 Project Structure
```
src/cpu_sim/
  cpu.py          # CPU core + ISA execution
  cache.py        # Cache simulation
  memory_bus.py   # Memory interface
  parser.py       # Instruction/data file parsing
  __main__.py     # CLI entrypoint
tests/            # Pytest suite
examples/         # Sample programs & data
```

---

## ✅ Testing
```bash
# run test suite
pytest -q --disable-warnings

# with coverage
pytest --cov=cpu_sim --cov-report=term-missing
```

---

## 📖 Documentation
See [Docs/](docs/) for:
- [System Architecture](docs/System_Architecture.md)
- [ISA Definition](docs/ISA_Definition.md)
- [Class Diagrams](docs/Class_Diagrams.md)
- [Use Cases](docs/Use_Cases.md)

---

## 📜 License
This project is licensed under the [MIT License](LICENSE).
