import heapq

def astar(graph, start, goal, heuristic):
    open_set = [(0, start)]
    came_from = {}
    g_score = {node: float('inf') for node in graph}
    g_score[start] = 0
    f_score = {node: float('inf') for node in graph}
    f_score[start] = heuristic[start]

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)    
            return path[::-1]
            

        for neighbor, cost in graph[current].items():
            tentative_g = g_score[current] + cost
            if tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic[neighbor]
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None

graph = {
    'A': {'B':1, 'C':3},
    'B': {'A':1, 'D':5},
    'C': {'A':3, 'D':1},
    'D': {'B':5, 'C':1}
}                

heuristic = {'A': 6, 'B': 4, 'C': 2, 'D': 0}
print(astar(graph, 'A', 'D', heuristic))

# Time Complexity: O(b^d)
# Space Complexity: O(b^d)
