def print_ordered_nodes(node_num, v1, v2, v3):
    ans = [
    node_num,
    node_num + v1,
    node_num + v2,
    node_num + v1 + v2,
    node_num + v3,
    node_num + v1 + v3,
    node_num + v2 + v3,
    node_num + v1 + v2 + v3
    ]
    print(ans)

# print_ordered_nodes(0, 1, 2, 4)

# face 0 is bottom
print_ordered_nodes(0,  1,  2,  4)
print_ordered_nodes(2, -2,  1,  4)
print_ordered_nodes(3, -1, -2,  4)
print_ordered_nodes(1,  2, -1,  4)

# face 1 is bottom
print_ordered_nodes(1, -1,  4,  2)
print_ordered_nodes(5, -4, -1,  2)
print_ordered_nodes(4,  1, -4,  2)
print_ordered_nodes(0,  4,  1,  2)

# face 2 is bottom
print_ordered_nodes(3, -2,  4, -1)
print_ordered_nodes(7, -4, -2, -1)
print_ordered_nodes(5,  2, -4, -1)
print_ordered_nodes(1,  4,  2, -1)

# face 3 is bottom
print_ordered_nodes(2,  1,  4, -2)
print_ordered_nodes(6, -4,  1, -2)
print_ordered_nodes(7, -1, -4, -2)
print_ordered_nodes(3,  4, -1, -2)

# face 4 is bottom
print_ordered_nodes(0,  2,  4,  1)
print_ordered_nodes(4, -4,  2,  1)
print_ordered_nodes(6, -2, -4,  1)
print_ordered_nodes(2,  4, -2,  1)

# face 5 is bottom
print_ordered_nodes(5, -1,  2, -4)
print_ordered_nodes(7, -2, -1, -4)
print_ordered_nodes(6,  1, -2, -4)
print_ordered_nodes(4,  2,  1, -4)

