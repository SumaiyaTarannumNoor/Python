def vertex_cover(graph):
    cover = set()
    edges = list(graph.keys())
    while edges:
        u, v = edges.pop()
        cover.add(v)
        edges = [(x, y) for (x, y) in edges if x not in cover and y not in cover]
    return cover


graph = {
    (1, 2): 1,
    (1, 3): 1,
    (2, 3): 1,
    (3, 4): 1,
}

print(vertex_cover(graph))

# Time Complexity: O(V + E)
# Space Complexity: O(V)
