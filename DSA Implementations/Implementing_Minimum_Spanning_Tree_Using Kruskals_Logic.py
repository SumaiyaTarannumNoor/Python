class UnioFind:
    def __init__(self, size):
        self.parent = list(range(size))

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        x_root = self.find(x)
        y_root = self.find(y)
        if x_root == y_root:
            return False
        self.parent[y_root] = x_root
        return True

def basic_mst_kruskal(graph):
    edges = []
    for u in graph:
        for v, weight in graph[u]:
            edges.append((weight, u, v))

    edges.sort()
    mst = []
    uf = UnioFind(len(graph))
    for weight, u, v in edges:
        if uf.union(u, v):
            mst.append((u, v, weight))
    return mst

graph = {
    0: [(1, 10), (2, 6), (3, 5)],
    1: [(0, 10), (3, 15)],
    2: [(0, 6), (3, 4)],
    3: [(0, 5), (1, 15), (2, 4)]
}

mst = basic_mst_kruskal(graph)
print("Basic MST (Kruskal's Logic): ")
for u, v, weight in mst:
    print(f"{u} -- {v} (Weight: {weight})")


# Time Complexity: O(E log V)
# Space Complexity: O(V + E)
# Auxiliary Space: O(V + E)