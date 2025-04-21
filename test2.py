import tkinter as tk
from tkinter import messagebox
import numpy as np
import heapq
import time
import matplotlib.pyplot as plt


def create_grid(rows, cols, obstacle_prob=0.3):
    grid = np.ones((rows, cols))
    for i in range(rows):
        for j in range(cols):
            if np.random.random() < obstacle_prob:
                grid[i, j] = float('inf')  # obstacle
    return grid


def optimal_path_dp(grid, start, goal):
    rows, cols = grid.shape
    cost = np.full((rows, cols), float('inf'))
    cost[start] = grid[start]
    parent = np.full((rows, cols, 2), -1)
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    queue = [(grid[start], start)]
    visited = set()

    start_time = time.time()

    while queue:
        curr_cost, (curr_r, curr_c) = heapq.heappop(queue)

        if (curr_r, curr_c) in visited:
            continue
        visited.add((curr_r, curr_c))

        if (curr_r, curr_c) == goal:
            break

        for dr, dc in directions:
            r, c = curr_r + dr, curr_c + dc
            if 0 <= r < rows and 0 <= c < cols and grid[r, c] != float('inf'):
                new_cost = curr_cost + grid[r, c]
                if new_cost < cost[r, c]:
                    cost[r, c] = new_cost
                    parent[r, c] = [curr_r, curr_c]
                    heapq.heappush(queue, (new_cost, (r, c)))

    execution_time = time.time() - start_time

    path = []
    if parent[goal][0] != -1:
        curr = goal
        while curr != start:
            path.append(curr)
            curr = tuple(parent[curr[0], curr[1]])
        path.append(start)
        path.reverse()

    return path, cost[goal], execution_time


def visualize_path(grid, path):
    plt.figure(figsize=(10, 8))
    plt.imshow(grid, cmap='viridis')
    if path:
        path_x = [p[1] for p in path]
        path_y = [p[0] for p in path]
        plt.plot(path_x, path_y, 'r-', linewidth=2)
        plt.plot(path_x[0], path_y[0], 'go', markersize=10)
        plt.plot(path_x[-1], path_y[-1], 'ro', markersize=10)
    plt.colorbar(label='Chi phí')
    plt.title('Robot Navigation: Đường đi tối ưu')
    plt.xlabel('Cột')
    plt.ylabel('Hàng')
    plt.grid(True)
    plt.show()


def run_algorithm():
    try:
        rows = int(entry_rows.get())
        cols = int(entry_cols.get())
        start_r = int(entry_start_r.get())
        start_c = int(entry_start_c.get())
        goal_r = int(entry_goal_r.get())
        goal_c = int(entry_goal_c.get())

        if not (0 <= start_r < rows and 0 <= start_c < cols and
                0 <= goal_r < rows and 0 <= goal_c < cols):
            messagebox.showerror("Lỗi", "Điểm bắt đầu hoặc kết thúc nằm ngoài lưới!")
            return

        start = (start_r, start_c)
        goal = (goal_r, goal_c)

        grid = create_grid(rows, cols)
        path, cost, exec_time = optimal_path_dp(grid, start, goal)

        if path:
            messagebox.showinfo("Kết quả", f"Tìm thấy đường đi\nChi phí: {cost:.2f}\nThời gian: {exec_time:.4f} giây")
            visualize_path(grid, path)
        else:
            messagebox.showwarning("Không thành công", "Không tìm thấy đường đi!")

    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập các số nguyên hợp lệ!")


# =======================
# Giao diện Tkinter
# =======================
root = tk.Tk()
root.title("Tìm đường đi tối ưu")

tk.Label(root, text="Số hàng (rows):").grid(row=0, column=0, sticky='e')
tk.Label(root, text="Số cột (cols):").grid(row=1, column=0, sticky='e')
tk.Label(root, text="Bắt đầu - hàng:").grid(row=2, column=0, sticky='e')
tk.Label(root, text="Bắt đầu - cột:").grid(row=3, column=0, sticky='e')
tk.Label(root, text="Kết thúc - hàng:").grid(row=4, column=0, sticky='e')
tk.Label(root, text="Kết thúc - cột:").grid(row=5, column=0, sticky='e')

entry_rows = tk.Entry(root)
entry_cols = tk.Entry(root)
entry_start_r = tk.Entry(root)
entry_start_c = tk.Entry(root)
entry_goal_r = tk.Entry(root)
entry_goal_c = tk.Entry(root)

entry_rows.grid(row=0, column=1)
entry_cols.grid(row=1, column=1)
entry_start_r.grid(row=2, column=1)
entry_start_c.grid(row=3, column=1)
entry_goal_r.grid(row=4, column=1)
entry_goal_c.grid(row=5, column=1)

tk.Button(root, text="Chạy thuật toán", command=run_algorithm).grid(row=6, column=0, columnspan=2, pady=10)

root.mainloop()
