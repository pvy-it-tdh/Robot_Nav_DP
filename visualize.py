import matplotlib.pyplot as plt

def visualize_path(grid, path):
    plt.figure(figsize=(10, 8))
    plt.imshow(grid, cmap='coolwarm')
    path_x = [p[1] for p in path]
    path_y = [p[0] for p in path]
    plt.plot(path_x, path_y, 'g-', linewidth=2)
    plt.scatter(path_x[0], path_y[0], color='red', label='Start', s=100)
    plt.scatter(path_x[-1], path_y[-1], color='blue', label='Goal', s=100)
    plt.colorbar(label='Chi phí')
    plt.title('Quy hoạch động: Đường đi tối ưu')
    plt.xlabel('Cột')
    plt.ylabel('Hàng')
    plt.legend()
    plt.grid(True)
    plt.show()