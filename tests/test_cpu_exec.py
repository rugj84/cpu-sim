from cpu_sim.memory_bus import MemoryBus
from cpu_sim.cache import Cache
from cpu_sim.cpu import CPU


def make_cpu(trace: bool = False) -> CPU:
    bus = MemoryBus()
    cache = Cache(bus=bus)
    return CPU(cache=cache, trace=trace)


def test_addi_then_add_execution():
    """
    Program:
      R1 <- R0 + 5
      R2 <- R1 + R1
      HALT
    Expect:
      R1 == 5, R2 == 10
    """
    cpu = make_cpu()
    program = [
        ("ADDI", ["R1", "R0", "5"]),
        ("ADD", ["R2", "R1", "R1"]),
        ("HALT", []),
    ]
    cpu.run(program)
    assert cpu.registers["R1"] == 5
    assert cpu.registers["R2"] == 10
    assert cpu.halted is True


def test_branch_and_jump_flow():
    """
    Program layout (indices):
      0: ADDI R1,R0,1     ; R1=1
      1: BNE  R1,R0, +2   ; taken -> skip next ADDI, jump to 4
      2: ADDI R2,R0,99    ; skipped
      3: J    5           ; skipped
      4: JAL  6           ; R7 <- 5, pc=6
      5: ADDI R3,R0,7     ; skipped (due to JAL)
      6: HALT
    """
    cpu = make_cpu()
    program = [
        ("ADDI", ["R1", "R0", "1"]),
        ("BNE", ["R1", "R0", "2"]),
        ("ADDI", ["R2", "R0", "99"]),
        ("J", ["5"]),
        ("JAL", ["6"]),
        ("ADDI", ["R3", "R0", "7"]),
        ("HALT", []),
    ]
    cpu.run(program)
    assert cpu.registers["R1"] == 1
    assert cpu.registers["R2"] == 0  # skipped
    assert cpu.registers["R3"] == 0  # skipped by JAL
    assert cpu.registers["R7"] == 5  # link after JAL
    assert cpu.halted


def test_cache_on_writeback_flush():
    """
    With cache ON:
      - Load MEM[8] (default 0), add 3, store back to MEM[8]
      - Data shouldn't hit MemoryBus until FLUSH
    """
    # Seed bus with address 8 -> 10
    bus = MemoryBus(memory={8: 10})
    cache = Cache(bus=bus)
    cpu = CPU(cache=cache, trace=False)

    program = [
        ("CACHE", ["1"]),             # enable cache
        ("LW", ["R1", "8(R0)"]),      # R1 <- 10
        ("ADDI", ["R1", "R1", "3"]),  # R1 <- 13
        ("SW", ["R1", "8(R0)"]),      # write-back to cache only
        ("HALT", []),
    ]
    cpu.run(program, max_steps=None)

    # At this point, without flush, MemoryBus should still be old value
    assert bus.read(8) == 10

    # Now flush and verify write-back reached MemoryBus
    cache.flush()
    assert bus.read(8) == 13
