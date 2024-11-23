const std = @import("std");


pub fn main(input: []const u8) void {
    const part1: u32 = 0;
    const part2: u32 = 0;

    var it = std.mem.splitScalar(u8, input, '\n');
    while (it.next()) |line| {
        _ = line;
    }

    std.debug.print("\n{s}\n", .{@src().file});
    std.debug.print("> {}\n", .{part1});
    std.debug.print("> {}\n", .{part2});
}
