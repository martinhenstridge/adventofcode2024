const std = @import("std");


const Day = struct {
    solver: fn ([]const u8) void,
    input: []const u8,
};


const days = [_]Day{
    .{
        .solver = @import("zig/day00.zig").main,
        .input = @embedFile("inputs/00"),
    },
};


pub fn main() !void {
    var should_run = [_]bool{false} ** days.len;
    var count: u8 = 0;

    var args = std.process.args();
    _ = args.skip();

    while (args.next()) |arg| {
        const idx = try std.fmt.parseUnsigned(u8, arg, 10);
        should_run[idx] = true;
        count += 1;
    }

    inline for (days[1..], 1..) |day, idx| {
        if (count == 0 or should_run[idx]) {
            day.solver(day.input);
        }
    }
}
