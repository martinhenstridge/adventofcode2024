const std = @import("std");
const Allocator = std.mem.Allocator;
const ArrayList = std.ArrayList;

fn extract_report(line: []const u8, report: *ArrayList(i32)) !void {
    var val_iter = std.mem.tokenizeScalar(u8, line, ' ');
    while (val_iter.next()) |val| {
        const level = try std.fmt.parseInt(i32, val, 10);
        try report.append(level);
    }
}

fn is_safe(report: []const i32) bool {
    const sign: i32 = if (report[0] > report[1]) 1 else -1;

    var pairs = std.mem.window(i32, report, 2, 1);
    while (pairs.next()) |pair| {
        const diff: i32 = (pair[0] - pair[1]) * sign;
        if (diff < 1 or diff > 3) {
            return false;
        }
    }

    return true;
}

fn write_damped_report(original: []const i32, omit: usize, target: *ArrayList(i32)) void {
    target.clearRetainingCapacity();
    for (original, 0..) |level, i| {
        if (i != omit) {
            target.appendAssumeCapacity(level);
        }
    }
}

fn is_safe_damped(original: []const i32, scratch: *ArrayList(i32)) bool {
    for (0..original.len) |omit| {
        write_damped_report(original, omit, scratch);
        if (is_safe(scratch.items)) {
            return true;
        }
    }
    return false;
}

pub fn main(allocator: Allocator, input: []const u8) !void {
    var safe_count_naive: u32 = 0;
    var safe_count_damped: u32 = 0;

    var report = ArrayList(i32).init(allocator);
    defer report.deinit();

    var scratch = ArrayList(i32).init(allocator);
    defer scratch.deinit();

    var lines = std.mem.tokenizeScalar(u8, input, '\n');
    while (lines.next()) |line| {
        report.clearRetainingCapacity();
        scratch.clearRetainingCapacity();

        try extract_report(line, &report);
        try scratch.ensureTotalCapacity(report.items.len);

        if (is_safe(report.items)) {
            safe_count_naive += 1;
            safe_count_damped += 1;
        } else if (is_safe_damped(report.items, &scratch)) {
            safe_count_damped += 1;
        }
    }

    std.debug.print("{}\n", .{safe_count_naive});
    std.debug.print("{}\n", .{safe_count_damped});
}
