from collections import deque
import heapq
from itertools import count

GRAPH = {
    'A': [('B', 2), ('C', 5)],
    'B': [('D', 4), ('E', 3)],
    'C': [('F', 2), ('G', 1)],
    'D': [], 'E': [], 'F': [], 'G': []
}

def bfs(start, goal):
    queue = deque([(start, [start])])
    visited = {start}
    order = []
    while queue:
        node, path = queue.popleft()
        order.append(node)
        if node == goal:
            return order, path
        for child, _ in GRAPH[node]:
            if child not in visited:
                visited.add(child)
                queue.append((child, path + [child]))
    return order, None

def dfs(start, goal):
    stack = [(start, [start])]
    visited = set()
    order = []
    while stack:
        node, path = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        order.append(node)
        if node == goal:
            return order, path
        for child, _ in reversed(GRAPH[node]):
            if child not in visited:
                stack.append((child, path + [child]))
    return order, None

def dls(start, goal, limit):
    order = []
    def visit(node, path, depth):
        order.append(node)
        if node == goal:
            return path
        if depth == limit:
            return None
        for child, _ in GRAPH[node]:
            if child not in path:
                result = visit(child, path + [child], depth + 1)
                if result is not None:
                    return result
        return None
    return order, visit(start, [start], 0)

def ids(start, goal, max_depth):
    for limit in range(max_depth + 1):
        order, path = dls(start, goal, limit)
        print('  Limit {}: {}'.format(limit, ' -> '.join(order)))
        if path is not None:
            return path
    return None

def ucs(start, goal):
    serial = count()
    frontier = [(0, next(serial), start, [start])]
    best_cost = {start: 0}
    order = []
    while frontier:
        cost, _, node, path = heapq.heappop(frontier)
        if cost != best_cost[node]:
            continue
        order.append(node)
        if node == goal:
            return order, path, cost
        for child, edge_cost in GRAPH[node]:
            new_cost = cost + edge_cost
            if new_cost < best_cost.get(child, float('inf')):
                best_cost[child] = new_cost
                heapq.heappush(frontier, (new_cost, next(serial), child, path + [child]))
    return order, None, None

def display(name, order, path):
    print('\n' + name)
    print('Visited: ' + ' -> '.join(order))
    print('Path: ' + (' -> '.join(path) if path else 'Not found'))

if __name__ == '__main__':
    start, goal = 'A', 'G'
    order, path = bfs(start, goal)
    display('BFS', order, path)
    order, path = dfs(start, goal)
    display('DFS', order, path)
    order, path = dls(start, goal, 1)
    display('DLS (limit = 1)', order, path)
    order, path = dls(start, goal, 2)
    display('DLS (limit = 2)', order, path)
    print('\nIDS')
    path = ids(start, goal, 3)
    print('Path: ' + (' -> '.join(path) if path else 'Not found'))
    order, path, cost = ucs(start, goal)
    display('UCS', order, path)
    print('Total cost:', cost)
