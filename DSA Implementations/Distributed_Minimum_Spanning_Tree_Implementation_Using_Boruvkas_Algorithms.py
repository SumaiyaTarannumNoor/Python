class Graph:
    def __init__(self, edges):
        self.edges = edges

class BoruvkaDistributedMST:
    def __init__(self, graph, nodes):
        self.graph = graph
        self.nodes = nodes
        
    def find_root(self, components, node):
        while components[node] != node:
            node = components[node]
        return node

    def union(self, components, root_u, root_v):
        components[root_v] = root_u

    def find_min_edge(self, node, components):
        min_edge = None
        min_weight = float('inf')
        component_root = self.find_root(components, node)
        for (u, v, weight) in self.graph.edges:
            root_u = self.find_root(components, u)        
            root_v = self.find_root(components, v)
            if root_u == component_root and root_v != component_root:
                if weight < min_weight:
                    min_weight = weight
                    min_edge = (u, v, weight)

        return min_edge

    def boruvka_distributed(self):
        components = {node: node for node in self.nodes}
        mst_edges = set()

        while len({self.find_root(components, node) for node in self.nodes}) > 1:
            min_edges = {}
            for node in self.nodes:
                component_root = self.find_root(components, node)
                min_edge = self.find_min_edge(node, components)
                if min_edge:
                    u, v, weight = min_edge
                    min_edges[component_root] = min_edge


            for edge in min_edges.values():
                u, v, _ = edge
                root_u = self.find_root(components, u)                    
                root_v = self.find_root(components, v)
                if root_u != root_v:
                    self.union(components, root_u, root_v)
                    mst_edges.add(edge)

        return mst_edges
                                    
edges = [
    (0, 1, 10),
    (0, 2, 6),
    (0, 3, 5),
    (1, 3, 15),
    (2, 3, 4)
]                


graph = Graph(edges)
nodes = {0, 1, 2, 3}

mst_finder = BoruvkaDistributedMST(graph, nodes)
mst_edges = mst_finder.boruvka_distributed()

print("Minimum Spanning Tree (Boruvka's Distributed Logic): ")
for u, v, weight in mst_edges:
    print(f"{u} -- {v} (Weight: {weight})")

# Time Complexity: O(E log V)
# Space Complexity: O(V + E)
# Auxiliary Space: O(v + E)    

