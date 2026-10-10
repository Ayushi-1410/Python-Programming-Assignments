MOD = 1000000007

n, m = map(int, input("Enter rows and columns: ").split())

grid = []

for _ in range(n):
    grid.append(input().split())

best = [[None] * m for _ in range(n)]
ways = [[0] * m for _ in range(n)]

if grid[0][0] != "X":
    best[0][0] = int(grid[0][0])
    ways[0][0] = 1

for i in range(n):
    for j in range(m):
        if grid[i][j] == "X" or (i == 0 and j == 0):
            continue

        score = int(grid[i][j])
        previous = []

        for pi, pj in [(i - 1, j), (i, j - 1), (i - 1, j - 1)]:
            if pi >= 0 and pj >= 0 and best[pi][pj] is not None:
                previous.append((best[pi][pj], ways[pi][pj]))

        if not previous:
            continue

        maximum = max(value for value, count in previous)
        best[i][j] = maximum + score

        ways[i][j] = sum(
            count for value, count in previous if value == maximum
        ) % MOD

if best[n - 1][m - 1] is None:
    print("IMPOSSIBLE")
else:
    print(best[n - 1][m - 1], ways[n - 1][m - 1])