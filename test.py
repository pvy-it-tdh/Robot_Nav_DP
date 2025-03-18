import numpy as np
import heapq
import time
import matplotlib.pyplot as plt
from memory_profiler import memory_usage


def create_grid(rows, cols, obstacle_prob=0.3):
    """Tạo lưới với chướng ngại vật ngẫu nhiên"""
    grid = np.ones((rows, cols))
    for i in range(rows):
        for j in range(cols):
            if np.random.random() < obstacle_prob:
                grid[i, j] = float('inf')  # Chướng ngại vật
    return grid


def optimal_path_dp(grid, start, goal):
    """Tìm đường đi tối ưu sử dụng quy hoạch động"""
    rows, cols = grid.shape

    # Khởi tạo ma trận chi phí
    cost = np.full((rows, cols), float('inf'))
    cost[start] = grid[start]

    # Khởi tạo ma trận cha cho việc tái tạo đường đi
    parent = np.full((rows, cols, 2), -1)

    # Các vector hướng
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # phải, xuống, trái, lên

    # Xử lý các ô theo thứ tự tăng dần khoảng cách từ điểm xuất phát
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

        # Kiểm tra cả bốn hướng
        for dr, dc in directions:
            r, c = curr_r + dr, curr_c + dc

            # Kiểm tra vị trí hợp lệ
            if 0 <= r < rows and 0 <= c < cols and grid[r, c] != float('inf'):
                new_cost = curr_cost + grid[r, c]

                if new_cost < cost[r, c]:
                    cost[r, c] = new_cost
                    parent[r, c] = [curr_r, curr_c]
                    heapq.heappush(queue, (new_cost, (r, c)))

    execution_time = time.time() - start_time

    # Tái tạo đường đi
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
    """Trực quan hóa lưới và đường đi tối ưu"""
    plt.figure(figsize=(10, 8))
    plt.imshow(grid, cmap='viridis')

    if path:
        path_x = [point[1] for point in path]
        path_y = [point[0] for point in path]
        plt.plot(path_x, path_y, 'r-', linewidth=2)
        plt.plot(path_x[0], path_y[0], 'go', markersize=10)  # Điểm bắt đầu
        plt.plot(path_x[-1], path_y[-1], 'ro', markersize=10)  # Điểm đích

    plt.colorbar(label='Chi phí')
    plt.title('Robot Navigation: Đường đi tối ưu')
    plt.xlabel('Cột')
    plt.ylabel('Hàng')
    plt.grid(True)
    plt.show(block=True)  # Giữ cửa sổ đồ thị mở


# ===========================
# Chạy thử nghiệm
# ===========================
if __name__ == "__main__":
    rows, cols = 20, 20
    start = (0, 0)
    goal = (19, 19)

    # Tạo lưới và tìm đường đi
    grid = create_grid(rows, cols)
    path, cost, execution_time = optimal_path_dp(grid, start, goal)

    # Hiển thị kết quả
    if path:
        print("Tìm thấy đường đi với chi phí:", cost)
        print("Thời gian thực thi:", execution_time, "giây")
        visualize_path(grid, path)
    else:
        print("Không tìm thấy đường đi.")