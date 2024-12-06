const std = @import("std");
const Allocator = std.mem.Allocator;
const ArrayList = std.ArrayList;
const AutoHashMap = std.AutoHashMap;

fn extract_rules(input: []const u8, rules: *AutoHashMap([2]u8, void)) !void {
    var rules_iter = std.mem.tokenizeScalar(u8, input, '\n');
    while (rules_iter.next()) |rule_text| {
        const a = try std.fmt.parseInt(u8, rule_text[0..2], 10);
        const b = try std.fmt.parseInt(u8, rule_text[3..5], 10);
        try rules.put(.{ a, b }, {});
    }
}

fn extract_pages(input: []const u8, pages: *ArrayList(u8)) !void {
    var page_iter = std.mem.tokenizeScalar(u8, input, ',');
    while (page_iter.next()) |page_text| {
        const page = try std.fmt.parseInt(u8, page_text, 10);
        try pages.append(page);
    }
}

fn sorter(rules: *AutoHashMap([2]u8, void), lhs: u8, rhs: u8) bool {
    if (rules.get(.{ lhs, rhs })) |_| {
        return true;
    }
    return false;
}

pub fn main(allocator: Allocator, input: []const u8) !void {
    var input_iter = std.mem.splitSequence(u8, input, "\n\n");
    const rules_input = input_iter.next().?;
    const pages_input = input_iter.next().?;

    var rules = AutoHashMap([2]u8, void).init(allocator);
    defer rules.deinit();
    try extract_rules(rules_input, &rules);

    var pages = ArrayList(u8).init(allocator);
    defer pages.deinit();

    var sorted = ArrayList(u8).init(allocator);
    defer sorted.deinit();

    var part1: u32 = 0;
    var part2: u32 = 0;

    var pages_iter = std.mem.tokenizeScalar(u8, pages_input, '\n');
    while (pages_iter.next()) |pages_text| {
        pages.clearRetainingCapacity();
        try extract_pages(pages_text, &pages);

        sorted.clearRetainingCapacity();
        try sorted.appendSlice(pages.items);

        std.mem.sort(u8, sorted.items, &rules, sorter);
        const middle = sorted.items[@divTrunc(sorted.items.len, 2)];

        if (std.mem.eql(u8, pages.items, sorted.items)) {
            part1 += middle;
        } else {
            part2 += middle;
        }
    }

    std.debug.print("{}\n", .{part1});
    std.debug.print("{}\n", .{part2});
}
