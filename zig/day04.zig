const std = @import("std");
const Allocator = std.mem.Allocator;
const ArrayList = std.ArrayList;

const Position = struct { row: i16, col: i16 };
const Direction = struct { dr: i8, dc: i8 };

const DIRECTIONS = [_]Direction{
    .{ .dr = -1, .dc = 0 },
    .{ .dr = 0, .dc = 1 },
    .{ .dr = 1, .dc = 0 },
    .{ .dr = 0, .dc = -1 },
    .{ .dr = -1, .dc = 1 },
    .{ .dr = 1, .dc = 1 },
    .{ .dr = 1, .dc = -1 },
    .{ .dr = -1, .dc = -1 },
};

fn extract_grid(input: []const u8, grid: *ArrayList([]const u8)) !void {
    var iter = std.mem.tokenizeScalar(u8, input, '\n');
    while (iter.next()) |line| {
        try grid.append(line);
    }
}

fn mas(grid: [][]const u8, start: Position, dir: Direction) bool {
    var r = start.row;
    var c = start.col;

    for ("MAS") |target| {
        if (r < 0 or r >= grid.len) {
            return false;
        }
        if (c < 0 or c >= grid[@intCast(r)].len) {
            return false;
        }
        if (grid[@intCast(r)][@intCast(c)] != target) {
            return false;
        }
        r += dir.dr;
        c += dir.dc;
    }

    return true;
}

fn xmas_count(grid: [][]const u8, p: Position) u32 {
    if (grid[@intCast(p.row)][@intCast(p.col)] != 'X') {
        return 0;
    }

    var count: u32 = 0;
    for (DIRECTIONS) |dir| {
        if (mas(grid, .{ .row = p.row + dir.dr, .col = p.col + dir.dc }, dir)) {
            count += 1;
        }
    }
    return count;
}

fn x_mas_count(grid: [][]const u8, p: Position) u32 {
    if (grid[@intCast(p.row)][@intCast(p.col)] != 'A') {
        return 0;
    }

    // Check for \-oriented MAS
    if (!(mas(grid, .{ .row = p.row - 1, .col = p.col - 1 }, .{ .dr = 1, .dc = 1 }) or
        mas(grid, .{ .row = p.row + 1, .col = p.col + 1 }, .{ .dr = -1, .dc = -1 })))
    {
        return 0;
    }

    // Check for /-oriented MAS
    if (!(mas(grid, .{ .row = p.row - 1, .col = p.col + 1 }, .{ .dr = 1, .dc = -1 }) or
        mas(grid, .{ .row = p.row + 1, .col = p.col - 1 }, .{ .dr = -1, .dc = 1 })))
    {
        return 0;
    }

    return 1;
}

pub fn main(allocator: Allocator, input: []const u8) !void {
    var count1: u32 = 0;
    var count2: u32 = 0;

    var grid = ArrayList([]const u8).init(allocator);
    defer grid.deinit();

    try extract_grid(input, &grid);
    for (0..grid.items.len) |r| {
        for (0..grid.items[r].len) |c| {
            const p = Position{ .row = @intCast(r), .col = @intCast(c) };
            count1 += xmas_count(grid.items, p);
            count2 += x_mas_count(grid.items, p);
        }
    }

    std.debug.print("{}\n", .{count1});
    std.debug.print("{}\n", .{count2});
}
