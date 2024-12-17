import re


def extract_registers(data: str) -> tuple[int, int, int]:
    ma = re.search(r"Register A: (\d+)", data)
    mb = re.search(r"Register B: (\d+)", data)
    mc = re.search(r"Register C: (\d+)", data)

    assert ma is not None
    assert mb is not None
    assert mc is not None

    return int(ma[1]), int(mb[1]), int(mc[1])


def extract_program(data: str) -> list[int]:
    mp = re.fullmatch(r"Program: ([\d\,]+)", data.strip())
    assert mp is not None
    return [int(i) for i in mp[1].split(",")]


def run_program_slow(program: list[int], a: int, b: int, c: int) -> list[int]:
    output: list[int] = []
    ip = 0

    def combo(operand: int) -> int:
        match operand:
            case 0 | 1 | 2 | 3:
                return operand
            case 4:
                return a
            case 5:
                return b
            case 6:
                return c
            case _:
                assert False

    while ip < len(program):
        opcode = program[ip]
        operand = program[ip + 1]
        ip += 2

        match opcode:
            case 0:
                a >>= combo(operand)
            case 1:
                b ^= operand
            case 2:
                b = combo(operand) & 7
            case 3:
                if a != 0:
                    ip = operand
            case 4:
                b ^= c
            case 5:
                output.append(combo(operand) & 7)
            case 6:
                b = a >> combo(operand)
            case 7:
                c = a >> combo(operand)

    return output


def run_program(program: list[int], a: int, b: int, c: int) -> list[int]:
    output: list[int] = []

    while a:
        b = a & 7
        b ^= 1
        c = a >> b
        a >>= 3
        b ^= 4
        b ^= c
        output.append(b & 7)

    return output


def search(program: list[int], a: int, b: int, c: int, matched: int = 0) -> int | None:
    if matched == len(program):
        return a

    a <<= 3
    for _ in range(8):
        output = run_program(program, a, b, c)
        if output == program[-len(output) :]:
            ret = search(program, a, b, c, matched + 1)
            if ret is not None:
                return ret
        a += 1

    return None


def run(data: str) -> None:
    register_input, program_input = data.split("\n\n")

    program = extract_program(program_input)
    a, b, c = extract_registers(register_input)

    output = run_program(program, a, b, c)
    string = ",".join(str(n) for n in output)

    quine = search(program, 0, b, c)

    print(string)
    print(quine)
