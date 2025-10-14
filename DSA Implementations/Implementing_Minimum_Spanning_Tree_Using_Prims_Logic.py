import heapq

def basic_mst_prim(graph):
    mst = []
    visited = set()
    start = 0
    heap = [(0, start, None)]
    while heap and len(visited) < len(graph):
        weight, u, parent = heapq.heappop(heap)
        if u in visited:
            continue
        visited.add(u)
        if parent is not None:
            mst.append((parent, u, weight))

        for v, w in graph[u]:
            if v not in visited:
                heapq.heappush(heap, (w, v, u))

    return mst


graph = {
    0: [(1, 10), (2, 6), (3, 5)],
    1: [(0, 10), (3, 15)],
    2: [(0, 6), (3, 4)],
    3: [(0, 5), (1, 15), (2, 4)]
}


mst = basic_mst_prim(graph)

print("Minimum Spanning Tree (Prim's Logic): ")
for parent, child, weight in mst:
    print(f"{parent} -- {child} (Weight: {weight})")


# Time Complexity: O(E log V)
# Space Complexity: O(V + E)
# Auxiliary Space: O(V + E)
