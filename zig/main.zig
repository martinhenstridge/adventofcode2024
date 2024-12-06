const std = @import("std");

const Problem = struct {
    input: []const u8,
    solver: fn (std.mem.Allocator, []const u8) anyerror!void,
};

const PROBLEMS = [_]Problem{
    .{ .input = "inputs/00", .solver = @import("./day00.zig").main },
    .{ .input = "inputs/01", .solver = @import("./day01.zig").main },
    .{ .input = "inputs/02", .solver = @import("./day02.zig").main },
    .{ .input = "inputs/03", .solver = @import("./day03.zig").main },
    .{ .input = "inputs/04", .solver = @import("./day04.zig").main },
    .{ .input = "inputs/05", .solver = @import("./day05.zig").main },
};

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{ .safety = true }){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();

    var should_run = [_]bool{false} ** PROBLEMS.len;
    var run_all: bool = true;
    var args = try std.process.argsWithAllocator(allocator);
    defer args.deinit();

    _ = args.skip();
    while (args.next()) |arg| {
        const day = try std.fmt.parseUnsigned(u8, arg, 10);
        if (day > 0 and day < PROBLEMS.len) {
            should_run[day] = true;
        }
        run_all = false;
    }

    inline for (PROBLEMS[1..], 1..) |problem, day| {
        if (run_all or should_run[day]) {
            const fd = try std.fs.cwd().openFile(problem.input, .{});
            defer fd.close();

            const stat = try fd.stat();
            const buffer = try fd.readToEndAlloc(allocator, stat.size);
            defer allocator.free(buffer);

            std.debug.print("Day {:0>2}\n======\n", .{day});
            var timer = try std.time.Timer.start();
            try problem.solver(allocator, buffer);
            std.debug.print("======\nt (ns) = {d}\n\n", .{timer.read()});
        }
    }
}
