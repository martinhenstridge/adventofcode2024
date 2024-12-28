import operator
import re
from typing import Any

OPS = {
    "AND": operator.and_,
    "OR": operator.or_,
    "XOR": operator.xor,
}


def extract_values(text: str) -> dict[str, int]:
    values = {}
    for line in text.splitlines():
        wire, value = line.split(": ", maxsplit=1)
        values[wire] = int(value)
    return values


def extract_connections(text: str) -> dict[str, tuple[str, str, str]]:
    connections = {}
    for m in re.finditer(r"(\w+) (AND|OR|XOR) (\w+) \-\> (\w+)", text):
        connections[m[4]] = (m[2], m[1], m[3])
    return connections


def simulate(
    connections: dict[str, tuple[str, str, str]], values: dict[str, int]
) -> int:
    known = values.copy()
    unknown = connections.copy()

    while unknown:
        still_unknown = {}
        for out, (op, a, b) in unknown.items():
            try:
                known[out] = OPS[op](known[a], known[b])
            except KeyError:
                still_unknown[out] = (op, a, b)
        unknown = still_unknown

    result = 0
    for k, v in known.items():
        if k.startswith("z"):
            idx = int(k[1:])
            result |= v << idx
    return result


def find_swapped_bits(connections: dict[str, tuple[str, str, str]]) -> list[str]:
    # The wires form a ripple adder. This works roughly as follows:
    #
    #     x_n XOR y_n => sum bit
    #     x_n AND y_n => carry bit
    #
    # The carry bit is propagated to the next wire along where it is eventually
    # XOR'd with the sum bit for that wire to produce the z bit.
    #
    # We can find swapped wires by finding inputs and outputs that do not
    # conform to this model.

    # Bits we'll need later...
    zlast = sorted(connections)[-1]
    sum_bits = {}
    carry_bits = {}
    for out, (op, a, b) in connections.items():
        match (op, a[0], b[0]):
            case ("XOR", "x", "y") | ("XOR", "y", "x"):
                sum_bits[out] = int(a[1:])
            case ("AND", "x", "y") | ("AND", "y", "x"):
                carry_bits[out] = int(a[1:])

    swapped = []
    for out, (op, a, b) in connections.items():
        # All z bits (except the last, which signifies overflow) are the output
        # of an XOR gate.
        if op != "XOR" and out.startswith("z") and out != zlast:
            swapped.append(out)

        # All XOR gates should either take x and y bits as input (to calculate
        # the sum bit) or output to z.
        if (
            op == "XOR"
            and not out.startswith("z")
            and not a.startswith("x")
            and not b.startswith("x")
        ):
            swapped.append(out)

        # Sum bits should never be inputs to OR gates.
        if op == "OR":
            if a in sum_bits:
                swapped.append(a)
            elif b in sum_bits:
                swapped.append(b)

        # Carry bits should never be inputs to AND gates, except the 0th where
        # the carry propagation is different.
        if op == "AND":
            if a in carry_bits and carry_bits[a] != 0:
                swapped.append(a)
            elif b in carry_bits and carry_bits[b] != 0:
                swapped.append(b)

    return swapped


def run(text: str) -> tuple[Any, Any]:
    values_text, connections_text = text.split("\n\n", maxsplit=1)

    values = extract_values(values_text)
    connections = extract_connections(connections_text)

    result = simulate(connections, values)
    swapped = find_swapped_bits(connections)

    return result, ",".join(sorted(swapped))
