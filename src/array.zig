const std = @import("std");

pub fn main() void {
    const capacity: u16 = 573;
    //_ = capacity;
    std.debug.print("{d}\n", .{capacity});
}
