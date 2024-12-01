const std = @import("std");
const Allocator = std.mem.Allocator;
const ArrayList = std.ArrayList;
const AutoHashMap = std.AutoHashMap;

fn extract_lists(input: []const u8, l1: *ArrayList(i32), l2: *ArrayList(i32)) !void {
    var line_iter = std.mem.splitScalar(u8, input, '\n');
    while (line_iter.next()) |line| {
        if (line.len == 0) {
            break;
        }

        var val_iter = std.mem.tokenizeScalar(u8, line, ' ');
        const n1 = try std.fmt.parseInt(i32, val_iter.next().?, 10);
        const n2 = try std.fmt.parseInt(i32, val_iter.next().?, 10);

        try l1.append(n1);
        try l2.append(n2);
    }
}

fn calculate_total_distance(l1: []const i32, l2: []const i32) u32 {
    var total: u32 = 0;
    for (l1, l2) |n1, n2| {
        total += @abs(n1 - n2);
    }
    return total;
}

fn calculate_similarity_score(allocator: Allocator, l1: []const i32, l2: []const i32) !i32 {
    var scores = AutoHashMap(i32, i32).init(allocator);
    defer scores.deinit();

    for (l2) |n| {
        if (scores.get(n)) |sum| {
            try scores.put(n, sum + n);
        } else {
            try scores.put(n, n);
        }
    }

    var total: i32 = 0;
    for (l1) |n| {
        if (scores.get(n)) |sum| {
            total += sum;
        }
    }
    return total;
}

pub fn main(allocator: Allocator, input: []const u8) !void {
    var l1 = ArrayList(i32).init(allocator);
    defer l1.deinit();

    var l2 = ArrayList(i32).init(allocator);
    defer l2.deinit();

    try extract_lists(input, &l1, &l2);
    std.debug.assert(l1.items.len == l2.items.len);
    std.mem.sort(i32, l1.items, {}, comptime std.sort.asc(i32));
    std.mem.sort(i32, l2.items, {}, comptime std.sort.asc(i32));

    const total_distance = calculate_total_distance(l1.items, l2.items);
    const similarity_score = try calculate_similarity_score(allocator, l1.items, l2.items);

    std.debug.print("{}\n", .{total_distance});
    std.debug.print("{}\n", .{similarity_score});
}
