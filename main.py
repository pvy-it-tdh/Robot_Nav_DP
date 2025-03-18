import tkinter as tk
from tkinter import messagebox
from find_optimal import find_optimal_dp
from visualize import visualize_path
import numpy as np

def on_find_path():
    try:
        input_text = text_area.get("1.0", tk.END).strip()
        rows = input_text.split("\n")
        cost_grid = []
        for row in rows:
            cost_grid.append([float(x) if x == 'inf' else int(x) for x in row.split()])

        cost_grid = np.array(cost_grid)
        optimal_cost, path = find_optimal_dp(cost_grid)

        if path:
            messagebox.showinfo("Kết quả", f"Chi phí tối ưu: {optimal_cost}")
            visualize_path(cost_grid, path)
        else:
            messagebox.showwarning("Kết quả", "Không tìm thấy đường đi khả thi.")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {e}")

root = tk.Tk()
root.title("Tìm Đường Đi Tối Ưu")
root.geometry("600x400")

label = tk.Label(root, text="Nhập ma trận chi phí (cách nhau bằng dấu cách, 'inf' cho vô cực):", anchor="w")
label.pack(fill="x")

text_area = tk.Text(root, height=10)
text_area.pack(fill="both", expand=True)

find_path_button = tk.Button(root, text="Tìm đường đi tối ưu", command=on_find_path)
find_path_button.pack(pady=10)

root.mainloop()