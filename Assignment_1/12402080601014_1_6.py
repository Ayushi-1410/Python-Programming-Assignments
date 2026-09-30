from collections import deque

print("PYTHON MODULE DEPENDENCY RESOLVER")

n = int(input("Enter number of modules: "))
e = int(input("Enter number of dependencies: "))

graph = {}
indegree = {}
modules = []

for i in range(n):
    name = input("Enter module " + str(i + 1) + ": ")
    modules.append(name)
    graph[name] = []
    indegree[name] = 0

for i in range(e):
    print("Dependency", i + 1)
    a = input("Module: ")
    b = input("Depends on: ")

    if b not in graph[a]:
        graph[a].append(b)
        indegree[b] += 1

queue = deque()

for name in modules:
    if indegree[name] == 0:
        queue.append(name)

answer = []

while queue:
    current = queue.popleft()
    answer.append(current)

    for next_module in graph[current]:
        indegree[next_module] -= 1

        if indegree[next_module] == 0:
            queue.append(next_module)

if len(answer) != n:
    print("CYCLE")
else:
    print("Loading Order:", " ".join(answer))