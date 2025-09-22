from __future__ import annotations

import argparse
from pathlib import Path

from .memory_bus import MemoryBus
from .cache import Cache
from .cpu import CPU


def main() -> None:
    parser = argparse.ArgumentParser(description="CS104 CPU Simulator")
    parser.add_argument(
        "--instructions",
        default=str(Path("instruction_input.txt")),
        help="Path to instruction file",
    )
    parser.add_argument(
        "--data",
        default=str(Path("data_input.txt")),
        help="Path to initial memory data file",
    )
    parser.add_argument(
        "--no-trace",
        action="store_true",
        help="Disable execution trace logs",
    )
    args = parser.parse_args()

    # 1) Load memory
    bus = MemoryBus()
    bus.load_from_file(args.data)

    # 2) Build cache
    cache = Cache(bus=bus)

    # 3) Build CPU
    cpu = CPU(cache=cache, trace=not args.no_trace)

    # 4) Load program
    program = CPU.parse_program(args.instructions)

    # 5) Execute
    print("[MAIN] Starting execution...")
    cpu.run(program)
    print("[MAIN] Execution finished.")

    # 6) Final state dump (brief)
    print("\n[STATE] Registers:")
    for r in sorted(cpu.registers.keys()):
        print(f"  {r} = {cpu.registers[r]}")
    print("\n[STATE] Memory (first 16 addresses present):")
    for addr in sorted(list(bus.memory.keys()))[:16]:
        print(f"  MEM[{addr}] = {bus.memory[addr]}")


if __name__ == "__main__":
    main()
