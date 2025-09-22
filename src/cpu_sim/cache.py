from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional

from .memory_bus import MemoryBus


@dataclass
class Cache:
    """
    Very simple (toy) cache layer. When 'on', acts as a small write-back cache.
    When 'off', reads/writes go directly to MemoryBus.
    - code 0: cache off
    - code 1: cache on
    - code 2: flush (write back and clear)

    This is a *pedagogical* cache, not an accurate hardware model.
    """

    bus: MemoryBus
    enabled: bool = False
    store: Dict[int, int] = field(default_factory=dict)

    def set_mode(self, code: int) -> None:
        if code == 0:
            print("[Cache] Mode -> OFF")
            # Flushing is optional when disabling; keep simple: write back & clear
            self.flush()
            self.enabled = False
        elif code == 1:
            print("[Cache] Mode -> ON")
            self.enabled = True
        elif code == 2:
            print("[Cache] FLUSH requested")
            self.flush()
        else:
            print(f"[Cache] Unknown code '{code}', ignoring.")

    def flush(self) -> None:
        if not self.store:
            print("[Cache] Nothing to flush.")
            return
        print(f"[Cache] Flushing {len(self.store)} entries to MemoryBus...")
        for addr, val in self.store.items():
            self.bus.write(addr, val)
        self.store.clear()
        print("[Cache] Flush complete.")

    def read(self, address: int) -> int:
        if self.enabled:
            if address in self.store:
                val = self.store[address]
                print(f"[Cache] HIT  [{address}] -> {val}")
                return val
            # miss -> fetch from bus
            val = self.bus.read(address)
            self.store[address] = val
            print(f"[Cache] MISS [{address}] -> fetched {val}")
            return val
        # bypass
        return self.bus.read(address)

    def write(self, address: int, value: int) -> None:
        if self.enabled:
            self.store[address] = value
            print(f"[Cache] WRITE-BACK [{address}] <- {value} (deferred to FLUSH)")
        else:
            self.bus.write(address, value)
