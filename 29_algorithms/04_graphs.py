"""Module 29 · Graphs: BFS, DFS, Dijkstra, topological sort

A GRAPH is nodes connected by edges: maps, social networks, task dependencies,
microservices calling each other. Store it as an ADJACENCY LIST: a dict
{node: [neighbours]}.

  BFS (breadth-first, a queue)  -> shortest path when every edge counts the same
  DFS (depth-first, a stack)    -> explore everything, find cycles, connected parts
  Dijkstra (a heap)             -> shortest path with WEIGHTED edges (km, ms, EUR)
  Topological sort              -> a valid order for tasks with dependencies

Run it:  python 29_algorithms/04_graphs.py
"""
import heapq
from collections import deque

# --- 1. BFS: fewest hops (who is "2 connections away" on LinkedIn?) --------------------------
friends = {
    "vishal": ["raj", "li"], "raj": ["vishal", "sam"], "li": ["vishal", "sam", "priya"],
    "sam": ["raj", "li", "mia"], "priya": ["li"], "mia": ["sam"],
}


def bfs_path(graph: dict, start: str, goal: str) -> list[str]:
    queue, came_from = deque([start]), {start: None}
    while queue:
        node = queue.popleft()
        if node == goal:                               # rebuild the path backwards
            path = []
            while node is not None:
                path.append(node)
                node = came_from[node]
            return path[::-1]
        for nxt in graph[node]:
            if nxt not in came_from:                   # never visit a node twice
                came_from[nxt] = node
                queue.append(nxt)
    return []


print("BFS vishal -> mia:", bfs_path(friends, "vishal", "mia"))


# --- 2. DFS: everything reachable, using an explicit stack ---------------------------------------
def dfs(graph: dict, start: str) -> list[str]:
    seen, stack, order = set(), [start], []
    while stack:
        node = stack.pop()
        if node in seen:
            continue
        seen.add(node)
        order.append(node)
        stack.extend(reversed(graph[node]))
    return order


print("DFS from vishal:  ", dfs(friends, "vishal"))

# --- 3. Dijkstra: cheapest route on a weighted graph (km between cities) -------------------------------
roads = {
    "Augsburg": {"Munich": 70, "Ulm": 85},
    "Munich": {"Augsburg": 70, "Nuremberg": 170, "Salzburg": 145},
    "Ulm": {"Augsburg": 85, "Stuttgart": 95},
    "Nuremberg": {"Munich": 170, "Stuttgart": 210},
    "Stuttgart": {"Ulm": 95, "Nuremberg": 210},
    "Salzburg": {"Munich": 145},
}


def dijkstra(graph: dict, start: str) -> dict[str, int]:
    best = {start: 0}
    heap = [(0, start)]                               # (distance so far, city)
    while heap:
        dist, city = heapq.heappop(heap)              # always the closest unfinished city
        if dist > best.get(city, float("inf")):
            continue                                  # an outdated entry: skip
        for nxt, km in graph[city].items():
            new = dist + km
            if new < best.get(nxt, float("inf")):
                best[nxt] = new
                heapq.heappush(heap, (new, nxt))
    return best


print("Dijkstra from Augsburg:", dict(sorted(dijkstra(roads, "Augsburg").items(), key=lambda kv: kv[1])))

# --- 4. Topological sort: an order that respects dependencies (build steps, courses) --------------------
needs = {"deploy": ["test", "build"], "test": ["install"], "build": ["install"], "install": []}


def topo_sort(deps: dict[str, list[str]]) -> list[str]:
    indegree = {task: len(before) for task, before in deps.items()}
    unlocks = {task: [] for task in deps}
    for task, before in deps.items():
        for b in before:
            unlocks[b].append(task)
    ready = deque(t for t, n in indegree.items() if n == 0)
    order = []
    while ready:
        task = ready.popleft()
        order.append(task)
        for nxt in unlocks[task]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                ready.append(nxt)
    if len(order) != len(deps):
        raise ValueError("cycle detected: no valid order")
    return order


print("build order:", topo_sort(needs))
