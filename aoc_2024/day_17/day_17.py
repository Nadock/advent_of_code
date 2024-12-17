def part_1(puzzle: str) -> int | str | float | bool:
    """Solution for AOC 2024, day 17, part 1."""
    cpu = CPU(
        int(puzzle.splitlines()[0].split(": ", 1)[1]),
        int(puzzle.splitlines()[1].split(": ", 1)[1]),
        int(puzzle.splitlines()[2].split(": ", 1)[1]),
    )
    cpu.execute([int(i) for i in puzzle.splitlines()[4].split(": ", 1)[1].split(",")])

    return ",".join([str(i) for i in cpu.output])


def part_2(puzzle: str) -> int | str | float | bool:
    """Solution for AOC 2024, day 17, part 2."""
    reg_b = int(puzzle.splitlines()[1].split(": ", 1)[1])
    reg_c = int(puzzle.splitlines()[2].split(": ", 1)[1])
    prog = [int(i) for i in puzzle.splitlines()[4].split(": ", 1)[1].split(",")]

    width = 1
    reg_a = 0
    while width <= len(prog):
        cpu = CPU(reg_a, reg_b, reg_c)
        cpu.execute(prog)

        if cpu.output == prog:
            break

        if cpu.output[len(cpu.output) - width :] == prog[len(prog) - width :]:
            width += 1
            reg_a *= 8
        else:
            reg_a += 1

    return reg_a


class CPU:
    def __init__(self, a: int, b: int, c: int) -> None:
        self.reg_a = a
        self.reg_b = b
        self.reg_c = c

        self.ptr = 0

        self.output: list[int] = []

    def execute(self, prog: list[int]) -> None:
        # print(prog)

        c = 0
        while self.ptr < len(prog):
            c += 1
            instr, op = prog[self.ptr], prog[self.ptr + 1]
            # print(
            #     f"BEFORE: {self.ptr=} -> {instr=} {op=} -> {self.reg_a} {self.reg_b} {self.reg_c}"
            # )
            self.dispatch(instr, op)

            # self.ptr += 2
            # print(
            #     f"AFTER: {self.ptr=} -> {instr=} {op=} -> {self.reg_a} {self.reg_b} {self.reg_c}",
            #     "\n   ",
            # )

            # if self.ptr == 4:
            #     break
            # if c > 10:
            #     break

    def dispatch(self, instr: int, op: int) -> None:
        if instr == 0:
            self.adv(op)
            self.ptr += 2
        elif instr == 1:
            self.bxl(op)
            self.ptr += 2
        elif instr == 2:
            self.bst(op)
            self.ptr += 2
        elif instr == 3:
            if not self.jnz(op):
                self.ptr += 2
        elif instr == 4:
            self.bxc(op)
            self.ptr += 2
        elif instr == 5:
            self.out(op)
            self.ptr += 2
        elif instr == 6:
            self.bdv(op)
            self.ptr += 2
        elif instr == 7:
            self.cdv(op)
            self.ptr += 2
        else:
            raise ValueError(f"Unknown instruction {instr}")

    def combo_operand(self, op: int) -> int:
        match op:
            case 0:
                return 0
            case 1:
                return 1
            case 2:
                return 2
            case 3:
                return 3
            case 4:
                return self.reg_a
            case 5:
                return self.reg_b
            case 6:
                return self.reg_c
            case _:
                raise ValueError(f"Unknown combo operand {op}")

    def adv(self, op: int) -> None:
        """
        The adv instruction (opcode 0) performs division. The numerator is the value in
        the A register. The denominator is found by raising 2 to the power of the
        instruction's combo operand. (So, an operand of 2 would divide A by 4 (2^2);
        an operand of 5 would divide A by 2^B.) The result of the division operation is
        truncated to an integer and then written to the A register.
        """
        num = self.reg_a
        den = 2 ** self.combo_operand(op)
        # print(f"  adv({op}): reg_a={num} // {den} == {num//den}")
        self.reg_a = num // den

    def bxl(self, op: int) -> None:
        """
        The bxl instruction (opcode 1) calculates the bitwise XOR of register B and the
        instruction's literal operand, then stores the result in register B.
        """
        self.reg_b = self.reg_b ^ op

    def bst(self, op: int) -> None:
        """
        The bst instruction (opcode 2) calculates the value of its combo operand modulo
        8 (thereby keeping only its lowest 3 bits), then writes that value to the B
        register.
        """
        self.reg_b = self.combo_operand(op) % 8

    def jnz(self, op: int) -> bool:
        """
        The jnz instruction (opcode 3) does nothing if the A register is 0. However, if
        the A register is not zero, it jumps by setting the instruction pointer to the
        value of its literal operand; if this instruction jumps, the instruction pointer
        is not increased by 2 after this instruction.
        """
        # print(f"  jnz({op})")
        if self.reg_a != 0:
            self.ptr = op
            return True
        return False

    def bxc(self, op: int) -> None:
        """
        The bxc instruction (opcode 4) calculates the bitwise XOR of register B and
        register C, then stores the result in register B. (For legacy reasons, this
        instruction reads an operand but ignores it).
        """
        del op
        self.reg_b = self.reg_b ^ self.reg_c

    def out(self, op: int) -> None:
        """
        The out instruction (opcode 5) calculates the value of its combo operand modulo
        8, then outputs that value. (If a program outputs multiple values, they are
        separated by commas).
        """
        # print(f"  out({op}) -> {self.combo_operand(op) % 8}")
        self.output.append(self.combo_operand(op) % 8)

    def bdv(self, op: int) -> None:
        """
        The bdv instruction (opcode 6) works exactly like the adv instruction except
        that the result is stored in the B register. (The numerator is still read from
        the A register).
        """
        num = self.reg_a
        den = 2 ** self.combo_operand(op)
        self.reg_b = num // den

    def cdv(self, op: int) -> None:
        """
        The cdv instruction (opcode 7) works exactly like the adv instruction except
        that the result is stored in the C register. (The numerator is still read from
        the A register).
        """
        num = self.reg_a
        den = 2 ** self.combo_operand(op)
        self.reg_c = num // den
