const std = @import("std");

const State = enum { enabled, disabled, digits1, digits2 };

fn match_literal(input: []const u8, index: *usize, literal: []const u8) bool {
    const i = index.*;
    const j = i + literal.len;

    if (j >= input.len) {
        return false;
    }

    if (std.mem.eql(u8, input[i..j], literal)) {
        index.* = j;
        return true;
    }

    return false;
}

fn match_do(input: []const u8, index: *usize) bool {
    return match_literal(input, index, "do()");
}

fn match_dont(input: []const u8, index: *usize) bool {
    return match_literal(input, index, "don't()");
}

fn match_mul(input: []const u8, index: *usize) bool {
    return match_literal(input, index, "mul(");
}

fn match_comma(input: []const u8, index: *usize) bool {
    return match_literal(input, index, ",");
}

fn match_close(input: []const u8, index: *usize) bool {
    return match_literal(input, index, ")");
}

fn match_digits(input: []const u8, index: *usize, match: *u32) bool {
    var digits: u32 = 0;
    var number: u32 = 0;

    for (0..3) |offset| {
        const i = index.* + offset;
        if (i >= input.len) {
            break;
        }

        const char = input[i];
        if (char < '0' or char > '9') {
            break;
        }

        digits += 1;
        number *= 10;
        number += char - '0';
    }

    index.* += digits;
    match.* = number;

    return digits > 0;
}

fn sum_multiplications(input: []const u8, conditionals: bool) u32 {
    var state = State.enabled;
    var mul1: u32 = undefined;
    var mul2: u32 = undefined;
    var total: u32 = 0;

    var i: usize = 0;
    while (i < input.len) {
        switch (state) {
            State.enabled => {
                if (match_do(input, &i)) {
                    continue;
                }
                if (match_dont(input, &i)) {
                    if (conditionals) {
                        state = State.disabled;
                    }
                    continue;
                }
                if (match_mul(input, &i)) {
                    state = State.digits1;
                    continue;
                }
            },
            State.disabled => {
                if (match_do(input, &i)) {
                    state = State.enabled;
                    continue;
                }
            },
            State.digits1 => {
                if (match_digits(input, &i, &mul1) and match_comma(input, &i)) {
                    state = State.digits2;
                } else {
                    state = State.enabled;
                }
                continue;
            },
            State.digits2 => {
                if (match_digits(input, &i, &mul2) and match_close(input, &i)) {
                    state = State.enabled;
                    total += mul1 * mul2;
                }
                state = State.enabled;
                continue;
            },
        }

        i += 1;
    }

    return total;
}

pub fn main(allocator: std.mem.Allocator, input: []const u8) !void {
    _ = allocator;

    const part1: u32 = sum_multiplications(input, false);
    const part2: u32 = sum_multiplications(input, true);

    std.debug.print("{}\n", .{part1});
    std.debug.print("{}\n", .{part2});
}
