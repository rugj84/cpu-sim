from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict


@dataclass
class MemoryBus:
    """
    Simple byte-addressable memory bus (integer address -> integer value).
    For this project, we treat addresses and values as Python ints.

    Data file format (example):
        00000001,4
        00000010,5

    Addresses may come in as binary strings; we parse base=2.
    """

    memory: Dict[int, int] = field(default_factory=dict)

    def load_from_file(self, path: str) -> None:
        print(f"[MemoryBus] Loading initial data from: {path}")
        with open(path, "r", encoding="utf-8") as f:
            for ln, raw in enumerate(f, start=1):
                line = raw.strip()
                if not line or line.startswith("#"):
                    continue
                addr_s, val_s = [t.strip() for t in line.split(",")]
                # Accept binary (e.g., 00000101) or decimal
                addr = int(addr_s, 2) if all(c in "01" for c in addr_s) else int(addr_s)
                val = int(val_s)
                self.memory[addr] = val
                print(f"[MemoryBus]  addr={addr} <- {val}  (line {ln})")
        print(f"[MemoryBus] Loaded {len(self.memory)} entries.")

    def read(self, address: int) -> int:
        val = self.memory.get(address, 0)
        print(f"[MemoryBus] READ  MEM[{address}] -> {val}")
        return val

    def write(self, address: int, value: int) -> None:
        self.memory[address] = value
        print(f"[MemoryBus] WRITE MEM[{address}] <- {value}")
