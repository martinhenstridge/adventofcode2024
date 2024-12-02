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

fn get_report_without(dst: []i32, src: []const i32, index: usize) void {
    std.debug.assert(dst.len == src.len - 1);
    var i: u32 = 0;
    for (0..src.len) |j| {
        if (j != index) {
            dst[i] = src[j];
            i += 1;
        }
    }
}

fn is_safe_damped(allocator: Allocator, report: []const i32) !bool {
    const damped = try allocator.alloc(i32, report.len - 1);
    defer allocator.free(damped);

    for (0..report.len) |i| {
        get_report_without(damped, report, i);
        if (is_safe(damped)) {
            return true;
        }
    }

    return false;
}

pub fn main(allocator: Allocator, input: []const u8) !void {
    var safe_count_naive: u32 = 0;
    var safe_count_damped: u32 = 0;

    var lines = std.mem.tokenizeScalar(u8, input, '\n');
    while (lines.next()) |line| {
        var report = ArrayList(i32).init(allocator);
        defer report.deinit();

        try extract_report(line, &report);
        if (is_safe(report.items)) {
            safe_count_naive += 1;
            safe_count_damped += 1;
        } else if (try is_safe_damped(allocator, report.items)) {
            safe_count_damped += 1;
        }
    }

    std.debug.print("{}\n", .{safe_count_naive});
    std.debug.print("{}\n", .{safe_count_damped});
}
