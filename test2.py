import tkinter as tk
from tkinter import messagebox
import numpy as np
import heapq
import time
import matplotlib.pyplot as plt


def create_grid(rows, cols, start=(0, 0), goal=None, obstacle_prob=0.3):
    """
    Create a grid with random obstacles.
    :param rows: Number of rows in the grid.
    :param cols: Number of columns in the grid.
    :param start: Starting position (row, col).
    :param goal: Goal position (row, col). If None, default to bottom-right corner.
    """
    if goal is None:
        goal = (rows - 1, cols - 1)

    grid = np.ones((rows, cols))

    for i in range(rows):
        for j in range(cols):
            if (i, j) == start or (i, j) == goal:
                continue  # No obstacles at start or goal

            rand = np.random.random()
            if rand < obstacle_prob:
                grid[i, j] = float('inf')  # Obstacle
            elif rand < obstacle_prob + 0.2:
                grid[i, j] = 5  # Mountain
            elif rand < obstacle_prob + 0.4:
                grid[i, j] = 2  # Sand
            else:
                grid[i, j] = 1  # Normal path

    return grid


# Function to find the optimal path using dynamic programming
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

        grid = create_grid(rows, cols, start=start, goal=goal)
        path, cost, exec_time = optimal_path_dp(grid, start, goal)

        if path:
            messagebox.showinfo("Kết quả", f"Tìm thấy đường đi\nChi phí: {cost:.2f}\nThời gian: {exec_time:.4f} giây")
            visualize_path(grid, path)
        else:
            messagebox.showwarning("Không thành công", "Không tìm thấy đường đi!")

    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập các số nguyên hợp lệ!")

        # ==== Giao diện Tkinter cải tiến ====
root = tk.Tk()
root.title("Tìm đường đi tối ưu")
root.geometry("320x300")
root.resizable(False, False)
root.configure(bg="#f0f2f5")

main_frame = tk.Frame(root)
main_frame.grid(row=0, column=0, sticky="nsew", padx=12, pady=12)


# Tiêu đề
tk.Label(main_frame, text="Thông số Lưới", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 10))

# Danh sách nhãn và entry
labels = [
    "Số hàng (rows):", "Số cột (cols):",
    "Bắt đầu - hàng:", "Bắt đầu - cột:",
    "Kết thúc - hàng:", "Kết thúc - cột:"
]

entries = []

for i, label in enumerate(labels):
    tk.Label(main_frame, text=label, font=("Arial", 10)).grid(row=i+1, column=0, sticky="e", padx=5, pady=5)
    entry = tk.Entry(main_frame, width=20)
    entry.grid(row=i+1, column=1, pady=5)
    entries.append(entry)

entry_rows, entry_cols, entry_start_r, entry_start_c, entry_goal_r, entry_goal_c = entries

# Nút chạy thuật toán
tk.Button(main_frame, text="Chạy thuật toán", command=run_algorithm).grid(row=7, column=0, columnspan=2, pady=15)

root.mainloop()