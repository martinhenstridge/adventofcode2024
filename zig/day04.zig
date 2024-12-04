const std = @import("std");
const Allocator = std.mem.Allocator;
const ArrayList = std.ArrayList;

const Direction = struct { dr: i8, dc: i8 };
const Position = struct {
    row: i16,
    col: i16,

    fn add(self: Position, dir: Direction) Position {
        return .{
            .row = self.row + dir.dr,
            .col = self.col + dir.dc,
        };
    }

    fn sub(self: Position, dir: Direction) Position {
        return .{
            .row = self.row - dir.dr,
            .col = self.col - dir.dc,
        };
    }
};

const U = Direction{ .dr = -1, .dc = 0 };
const R = Direction{ .dr = 0, .dc = 1 };
const D = Direction{ .dr = 1, .dc = 0 };
const L = Direction{ .dr = 0, .dc = -1 };

const UR = Direction{ .dr = -1, .dc = 1 };
const DR = Direction{ .dr = 1, .dc = 1 };
const DL = Direction{ .dr = 1, .dc = -1 };
const UL = Direction{ .dr = -1, .dc = -1 };

const DIRECTIONS = [_]Direction{
    U,  D,  L,  R,
    UR, DR, DL, UL,
};

fn extract_grid(input: []const u8, grid: *ArrayList([]const u8)) !void {
    var iter = std.mem.tokenizeScalar(u8, input, '\n');
    while (iter.next()) |line| {
        try grid.append(line);
    }
}

fn not_match(grid: [][]const u8, p: Position, target: u8) bool {
    return grid[@intCast(p.row)][@intCast(p.col)] != target;
}

fn mas(grid: [][]const u8, start: Position, dir: Direction) bool {
    var p = start;

    for ("MAS") |target| {
        if (p.row < 0 or p.row >= grid.len) {
            return false;
        }
        if (p.col < 0 or p.col >= grid.len) {
            return false;
        }
        if (not_match(grid, p, target)) {
            return false;
        }
        p = p.add(dir);
    }

    return true;
}

fn xmas_count(grid: [][]const u8, p: Position) u32 {
    if (not_match(grid, p, 'X')) {
        return 0;
    }

    var count: u32 = 0;
    for (DIRECTIONS) |dir| {
        if (mas(grid, p.add(dir), dir)) {
            count += 1;
        }
    }
    return count;
}

fn x_mas_count(grid: [][]const u8, p: Position) u32 {
    // All X-MAS instances have an A at the centre
    if (not_match(grid, p, 'A')) {
        return 0;
    }

    // Check for \-oriented MAS
    if (!(mas(grid, p.sub(DR), DR) or mas(grid, p.sub(UL), UL))) {
        return 0;
    }

    // Check for /-oriented MAS
    if (!(mas(grid, p.sub(DL), DL) or mas(grid, p.sub(UR), UR))) {
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
        for (0..grid.items.len) |c| {
            const p = Position{ .row = @intCast(r), .col = @intCast(c) };
            count1 += xmas_count(grid.items, p);
            count2 += x_mas_count(grid.items, p);
        }
    }

    std.debug.print("{}\n", .{count1});
    std.debug.print("{}\n", .{count2});
}
