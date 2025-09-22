from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Optional

from .cache import Cache


Register = str
Instruction = Tuple[str, List[str]]  # (mnemonic, [operands...])


def parse_register(token: str) -> Register:
    t = token.strip().upper()
    if not t.startswith("R"):
        raise ValueError(f"Expected register like R2, got '{token}'")
    return t


def parse_int(token: str) -> int:
    t = token.strip()
    # Allow 0b-like binary strings without prefix (e.g., "00000101")
    if t and all(c in "01" for c in t):
        try:
            return int(t, 2)
        except ValueError:
            pass
    return int(t)


@dataclass
class CPU:
    """
    Minimal CPU skeleton with:
    - 8 general-purpose registers: R0..R7 (R0 hardwired to 0 on write)
    - PC measured in *instruction indices* (not bytes)
    - ISA subset per assignment (ADD, ADDI, SUB, SLT, BNE, J, JAL, LW, SW, CACHE, HALT).

    Design notes:
    - We treat PC as an index into the instruction list.
    - BNE offset is relative to the *next* instruction (MIPS-like), measured in instructions.
    - J/JAL 'target' is an absolute instruction index (not bytes).
    - JAL stores the link (PC+1) into R7.
    - LW/SW compute address = Rs + offset (integers).
    """

    cache: Cache
    registers: Dict[Register, int] = field(default_factory=lambda: {f"R{i}": 0 for i in range(8)})
    pc: int = 0
    halted: bool = False
    trace: bool = True

    def reset(self) -> None:
        for k in self.registers:
            self.registers[k] = 0
        self.pc = 0
        self.halted = False

    # --- Instruction loading/parsing ---

    @staticmethod
    def parse_program(path: str) -> List[Instruction]:
        """
        File format:
            <MNEMONIC>,<ARG1>,...,<ARGn>
        e.g.
            ADDI,R2,R2,2
            CACHE,1
            HALT,;
        """
        program: List[Instruction] = []
        print(f"[CPU] Loading instructions from: {path}")
        with open(path, "r", encoding="utf-8") as f:
            for ln, raw in enumerate(f, start=1):
                line = raw.strip()
                if not line or line.startswith("#"):
                    continue
                parts = [p.strip() for p in line.split(",")]
                mnemonic = parts[0].upper()
                # Some lines might put ';' as a placeholder (e.g., HALT,;)
                operands = [p for p in parts[1:] if p and p != ";"]
                program.append((mnemonic, operands))
                print(f"[CPU]  {ln:>3}: {mnemonic} {operands}")
        print(f"[CPU] Loaded {len(program)} instructions.")
        return program

    # --- Execution loop ---

    def run(self, program: List[Instruction], max_steps: Optional[int] = None) -> None:
        steps = 0
        while not self.halted and 0 <= self.pc < len(program):
            if max_steps is not None and steps >= max_steps:
                print("[CPU] Max steps reached; stopping.")
                break
            self.step(program)
            steps += 1
        if self.halted:
            print("[CPU] Execution halted.")
        else:
            print("[CPU] Program ended (pc out of range).")

    def step(self, program: List[Instruction]) -> None:
        instr, ops = program[self.pc]
        if self.trace:
            print(f"[CPU] PC={self.pc}  EXEC: {instr} {ops}")
        self.pc += 1  # pre-increment like MIPS (PC points to next by default)

        # Dispatch
        handler = getattr(self, f"_op_{instr}", None)
        if handler is None:
            raise NotImplementedError(f"Instruction '{instr}' not implemented.")
        handler(ops)

    # --- Helpers ---

    def _read_reg(self, r: Register) -> int:
        return self.registers.get(r, 0)

    def _write_reg(self, r: Register, value: int) -> None:
        if r == "R0":
            # R0 is hardwired to 0
            if self.trace:
                print("[CPU] Ignoring write to R0 (hardwired zero).")
            return
        self.registers[r] = value

    # --- ISA implementations (skeletons with working behavior) ---

    def _op_ADD(self, ops: List[str]) -> None:
        # ADD Rd, Rs, Rt
        rd, rs, rt = map(parse_register, ops)
        res = self._read_reg(rs) + self._read_reg(rt)
        self._write_reg(rd, res)
        if self.trace:
            print(f"[CPU] {rd} <- {res}  (ADD {rs} + {rt})")

    def _op_ADDI(self, ops: List[str]) -> None:
        # ADDI Rt, Rs, immd
        rt, rs, immd_s = ops[0], ops[1], ops[2]
        rt, rs = parse_register(rt), parse_register(rs)
        immd = parse_int(immd_s)
        res = self._read_reg(rs) + immd
        self._write_reg(rt, res)
        if self.trace:
            print(f"[CPU] {rt} <- {res}  (ADDI {rs} + {immd})")

    def _op_SUB(self, ops: List[str]) -> None:
        # SUB Rd, Rs, Rt
        rd, rs, rt = map(parse_register, ops)
        res = self._read_reg(rs) - self._read_reg(rt)
        self._write_reg(rd, res)
        if self.trace:
            print(f"[CPU] {rd} <- {res}  (SUB {rs} - {rt})")

    def _op_SLT(self, ops: List[str]) -> None:
        # SLT Rd, Rs, Rt
        rd, rs, rt = map(parse_register, ops)
        res = 1 if self._read_reg(rs) < self._read_reg(rt) else 0
        self._write_reg(rd, res)
        if self.trace:
            print(f"[CPU] {rd} <- {res}  (SLT {rs} < {rt})")

    def _op_BNE(self, ops: List[str]) -> None:
        # BNE Rs, Rt, offset   -> if Rs != Rt then PC <- PC + offset
        rs, rt, off_s = ops[0], ops[1], ops[2]
        rs, rt = parse_register(rs), parse_register(rt)
        off = parse_int(off_s)
        if self._read_reg(rs) != self._read_reg(rt):
            old_pc = self.pc
            self.pc = self.pc + off
            if self.trace:
                print(f"[CPU] BNE taken: PC {old_pc} -> {self.pc}")
        else:
            if self.trace:
                print("[CPU] BNE not taken")

    def _op_J(self, ops: List[str]) -> None:
        # J target  (absolute instruction index)
        target = parse_int(ops[0])
        if self.trace:
            print(f"[CPU] JUMP to {target}")
        self.pc = target

    def _op_JAL(self, ops: List[str]) -> None:
        # JAL target: R7 <- PC; PC <- target
        target = parse_int(ops[0])
        link = self.pc  # already incremented
        self._write_reg("R7", link)
        if self.trace:
            print(f"[CPU] JAL link R7 <- {link}, JUMP to {target}")
        self.pc = target

    def _op_LW(self, ops: List[str]) -> None:
        # LW Rt, offset(Rs)
        # Example: LW R2, 8(R1)
        rt = parse_register(ops[0])
        off, rs = self._parse_mem_operand(ops[1])
        addr = self._read_reg(rs) + off
        val = self.cache.read(addr)
        self._write_reg(rt, val)
        if self.trace:
            print(f"[CPU] {rt} <- MEM[{addr}] ({val})")

    def _op_SW(self, ops: List[str]) -> None:
        # SW Rt, offset(Rs)
        rt = parse_register(ops[0])
        off, rs = self._parse_mem_operand(ops[1])
        addr = self._read_reg(rs) + off
        val = self._read_reg(rt)
        self.cache.write(addr, val)
        if self.trace:
            print(f"[CPU] MEM[{addr}] <- {val}")

    def _op_CACHE(self, ops: List[str]) -> None:
        # CACHE code   (0=off, 1=on, 2=flush)
        code = parse_int(ops[0])
        self.cache.set_mode(code)

    def _op_HALT(self, ops: List[str]) -> None:
        self.halted = True
        if self.trace:
            print("[CPU] HALT")

    # --- parsing helpers ---

    @staticmethod
    def _parse_mem_operand(token: str) -> Tuple[int, Register]:
        """
        Parse 'offset(Rs)' -> (offset:int, 'Rs')
        """
        t = token.strip()
        if "(" not in t or not t.endswith(")"):
            raise ValueError(f"Bad memory operand: '{token}'")
        off_s, reg_s = t.split("(", 1)
        reg = reg_s[:-1]  # strip ')'
        return parse_int(off_s), parse_register(reg)
