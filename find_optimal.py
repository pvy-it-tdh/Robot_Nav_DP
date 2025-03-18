import numpy as np

def find_optimal_dp(cost_grid):
    m, n = len(cost_grid), len(cost_grid[0])
    dp = np.zeros((m, n), dtype=int)
    parent = np.full((m, n, 2), -1)

    dp[0][0] = cost_grid[0][0]

    for j in range(1, n):
        if cost_grid[0][j] != float('inf'):
            dp[0][j] = dp[0][j - 1] + cost_grid[0][j]
            parent[0][j] = (0, j - 1)
        else:
            dp[0][j] = float('inf')

    for i in range(1, m):
        if cost_grid[i][0] != float('inf'):
            dp[i][0] = dp[i - 1][0] + cost_grid[i][0]
            parent[i][0] = (i - 1, 0)
        else:
            dp[i][0] = float('inf')

    for i in range(1, m):
        for j in range(1, n):
            if cost_grid[i][j] != float('inf'):
                from_top = dp[i - 1][j] if dp[i - 1][j] != float('inf') else float('inf')
                from_left = dp[i][j - 1] if dp[i][j - 1] != float('inf') else float('inf')
                dp[i][j] = cost_grid[i][j] + min(from_top, from_left)
                if from_top <= from_left:
                    parent[i][j] = (i - 1, j)
                else:
                    parent[i][j] = (i, j - 1)
            else:
                dp[i][j] = float('inf')

    path = []
    i, j = m - 1, n - 1
    while (i, j) != (0, 0):
        if parent[i][j][0] == -1:
            path = []
            break
        path.append((i, j))
        i, j = parent[i][j]
    if path:
        path.append((0, 0))
        path.reverse()

    return dp[-1][-1], path