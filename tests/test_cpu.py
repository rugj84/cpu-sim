
from cpu_sim.cpu import CPU

def test_cpu_initialization():
    cpu = CPU()
    assert cpu.PC == 0
    assert isinstance(cpu.registers, dict)
