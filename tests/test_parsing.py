from pathlib import Path

from cpu_sim.cpu import CPU
from cpu_sim.memory_bus import MemoryBus


def test_parse_program_basic(tmp_path: Path):
    content = "\n".join(
        [
            "  # comment",
            "ADDI , R2 , R2 , 2",
            "CACHE,1",
            "HALT,;",
        ]
    )
    f = tmp_path / "prog.txt"
    f.write_text(content, encoding="utf-8")

    program = CPU.parse_program(str(f))
    assert program == [
        ("ADDI", ["R2", "R2", "2"]),
        ("CACHE", ["1"]),
        ("HALT", []),
    ]


def test_memory_bus_load_and_rw(tmp_path: Path):
    # Mix binary and decimal addresses
    content = "\n".join(
        [
            "00000001,4",
            "16,99",
            "00000010,5",
        ]
    )
    f = tmp_path / "data.txt"
    f.write_text(content, encoding="utf-8")

    bus = MemoryBus()
    bus.load_from_file(str(f))

    # Binary "00000001" -> 1
    assert bus.read(1) == 4
    # Decimal 16 remains 16
    assert bus.read(16) == 99

    # Write + read back
    bus.write(3, 123)
    assert bus.read(3) == 123
