import tkinter as tk
from tkinter import messagebox
import numpy as np
import heapq
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


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
                continue
            rand = np.random.random()
            if rand < obstacle_prob:
                grid[i, j] = float('inf')
            elif rand < obstacle_prob + 0.2:
                grid[i, j] = 5
            elif rand < obstacle_prob + 0.4:
                grid[i, j] = 2
            else:
                grid[i, j] = 1
    return grid


def hybrid_dp_dijkstra(grid, start, goal):
    rows, cols = grid.shape
    INF = float('inf')
    dp = np.full((rows, cols), INF)
    parent = np.full((rows, cols, 2), -1)

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    queue = []

    start_time = time.time()

    # === Phase 1: DP khởi tạo theo hướng phải và xuống ===
    dp[start] = grid[start]
    for i in range(start[0], rows):
        for j in range(start[1], cols):
            if (i, j) == start or grid[i, j] == INF:
                continue
            if i > 0 and grid[i-1, j] != INF and dp[i, j] > dp[i-1, j] + grid[i, j]:
                dp[i, j] = dp[i-1, j] + grid[i, j]
                parent[i, j] = [i-1, j]
            if j > 0 and grid[i, j-1] != INF and dp[i, j] > dp[i, j-1] + grid[i, j]:
                dp[i, j] = dp[i, j-1] + grid[i, j]
                parent[i, j] = [i, j-1]

    # === Phase 2: Dijkstra tiếp tục mở rộng từ kết quả DP ===
    visited = set()
    for i in range(rows):
        for j in range(cols):
            if dp[i, j] != INF:
                heapq.heappush(queue, (dp[i, j], (i, j)))

    while queue:
        curr_cost, (curr_r, curr_c) = heapq.heappop(queue)
        if (curr_r, curr_c) in visited:
            continue
        visited.add((curr_r, curr_c))

        if (curr_r, curr_c) == goal:
            break

        for dr, dc in directions:
            r, c = curr_r + dr, curr_c + dc
            if 0 <= r < rows and 0 <= c < cols and grid[r, c] != INF:
                new_cost = curr_cost + grid[r, c]
                if new_cost < dp[r, c]:
                    dp[r, c] = new_cost
                    parent[r, c] = [curr_r, curr_c]
                    heapq.heappush(queue, (new_cost, (r, c)))

    execution_time = time.time() - start_time

    # === Truy vết đường đi ===
    path = []
    if parent[goal][0] != -1:
        curr = goal
        while tuple(curr) != start:
            path.append(tuple(curr))
            curr = parent[curr[0], curr[1]]
        path.append(start)
        path.reverse()

    return path, dp[goal], execution_time


def visualize_path_tk(grid, path, canvas_frame):
    # Xóa các plot trước đó nếu có
    for widget in canvas_frame.winfo_children():
        widget.destroy()

    fig, ax = plt.subplots(figsize=(5, 4))
    ax.imshow(grid, cmap='viridis')
    # Hiển thị chi phí của từng ô trên lưới
    rows, cols = grid.shape
    for i in range(rows):
        for j in range(cols):
            value = grid[i, j]
            if value == float('inf'):
                text = "∞"
                color = "black"
            else:
                text = str(int(value)) if value == int(value) else f"{value:.1f}"
                # Đổi màu chữ tùy theo mức chi phí
                if value > 5:
                    color = "white"
                elif value >= 2:
                    color = "#003366"  # xanh đậm
                else:
                    color = "black"
            ax.text(j, i, text, ha='center', va='center', color=color, fontsize=9, fontweight='bold')

    if path:
        path_x = [p[1] for p in path]
        path_y = [p[0] for p in path]
        ax.plot(path_x, path_y, 'r-', linewidth=2)
        ax.plot(path_x[0], path_y[0], 'go', markersize=10)
        ax.plot(path_x[-1], path_y[-1], 'ro', markersize=10)

    ax.set_title('Đường đi tối ưu')
    ax.set_xlabel('Cột')
    ax.set_ylabel('Hàng')
    ax.grid(True)

    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()


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
        path, cost, exec_time = hybrid_dp_dijkstra(grid, start, goal)

        if path:
            result_label.config(
                text=f"✅ Đã tìm thấy đường đi\nChi phí: {cost:.2f}\nThời gian: {exec_time:.4f} giây",
                fg="green")
        else:
            result_label.config(text="❌  Không tìm thấy đường đi!", fg="red")

        visualize_path_tk(grid, path, canvas_frame)

    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập các số nguyên hợp lệ!")


# ==== Giao diện Tkinter ==== #
root = tk.Tk()
root.title("🚀 Tìm đường đi tối ưu")
root.geometry("1000x700")
root.configure(bg="#e8eff1")

# Style chung
default_font = ("Segoe UI", 11)
label_font = ("Segoe UI", 12)
title_font = ("Segoe UI", 16, "bold")

# Khung nhập liệu bên trái
input_frame = tk.Frame(root, bg="#ffffff", bd=2, relief="ridge")
input_frame.pack(side="left", padx=20, pady=20, fill="y")

tk.Label(input_frame, text="🔧 Thông số Lưới", font=title_font, bg="#ffffff", fg="#333").pack(pady=(10, 15))

labels = [
    "Số hàng (rows):", "Số cột (cols):",
    "Bắt đầu - hàng:", "Bắt đầu - cột:",
    "Kết thúc - hàng:", "Kết thúc - cột:"
]
entries = []

for i, label in enumerate(labels):
    tk.Label(input_frame, text=label, bg="#ffffff", font=label_font, anchor="w").pack(fill="x", padx=10)
    entry = tk.Entry(input_frame, width=22, font=default_font, bg="#f5f5f5", relief="groove", bd=1)
    entry.pack(pady=5, padx=10)
    entries.append(entry)

entry_rows, entry_cols, entry_start_r, entry_start_c, entry_goal_r, entry_goal_c = entries

tk.Button(
    input_frame, text="▶ Chạy thuật toán", command=run_algorithm,
    bg="#007acc", fg="white", font=label_font, bd=0, padx=10, pady=5, activebackground="#005f99"
).pack(pady=20)

result_label = tk.Label(input_frame, text="", font=("Segoe UI", 10, "bold"), bg="#ffffff")
result_label.pack(pady=5)

# Khung hiển thị biểu đồ bên phải
canvas_frame = tk.Frame(root, bg="#e8eff1")
canvas_frame.pack(side="right", expand=True, fill="both", padx=10, pady=20)
root.mainloop()
