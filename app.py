import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np

def northwest_corner(costs, supply, demand):
    supply = np.array(supply)
    demand = np.array(demand)

    if sum(supply) != sum(demand):
        return None, f"Задача не сбалансирована. Сумма поставок ({sum(supply)}) не равна сумме потребностей ({sum(demand)})."

    num_suppliers = len(supply)
    num_consumers = len(demand)
    allocation = np.zeros((num_suppliers, num_consumers), dtype=int)
    total_cost = 0
    
    i, j = 0, 0 
    while i < num_suppliers and j < num_consumers:
        quantity = min(supply[i], demand[j])
        allocation[i, j] = quantity
        total_cost += costs[i, j] * quantity
    
        supply[i] -= quantity
        demand[j] -= quantity
    
        if supply[i] == 0:
            i += 1
        else:
            j += 1
    
    return allocation, total_cost

def solve_and_display():
    try:
        costs_str = costs_text.get("1.0", "end-1c")
        supply_str = supply_entry.get()
        demand_str = demand_entry.get()

        costs = np.array([list(map(int, row.split())) for row in costs_str.splitlines()])
        supply = list(map(int, supply_str.split()))
        demand = list(map(int, demand_str.split()))

        result = northwest_corner(costs, supply, demand)

        if result[0] is not None:
            allocation, total_cost = result
            result_text.config(state=tk.NORMAL)
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, "Базисный план (метод северо-западного угла):\n")
            for row in allocation:
                result_text.insert(tk.END, str(row) + "\n")
            result_text.insert(tk.END, f"\nОбщие затраты: {total_cost}")
            result_text.config(state=tk.DISABLED)
        else:
             messagebox.showerror("Ошибка", result[1])
             result_text.config(state=tk.NORMAL)
             result_text.delete(1.0, tk.END)
             result_text.config(state=tk.DISABLED)
    except ValueError:
        messagebox.showerror("Ошибка", "Некорректный формат ввода")
        result_text.config(state=tk.NORMAL)
        result_text.delete(1.0, tk.END)
        result_text.config(state=tk.DISABLED)

root = tk.Tk()
root.title("Транспортная задача")

# --- Labels and input fields ---
ttk.Label(root, text="Матрица затрат: (строки через Enter, числа через пробел)").grid(row=0, column=0, sticky="w", padx=5, pady=5)
costs_text = tk.Text(root, height=5, width=40)
costs_text.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(root, text="Поставки (через пробел):").grid(row=1, column=0, sticky="w", padx=5, pady=5)
supply_entry = ttk.Entry(root, width=40)
supply_entry.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(root, text="Потребности (через пробел):").grid(row=2, column=0, sticky="w", padx=5, pady=5)
demand_entry = ttk.Entry(root, width=40)
demand_entry.grid(row=2, column=1, padx=5, pady=5)


solve_button = ttk.Button(root, text="Решить", command=solve_and_display)
solve_button.grid(row=3, column=0, columnspan=2, pady=10)

ttk.Label(root, text="Результат:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
result_text = tk.Text(root, height=10, width=60, state=tk.DISABLED)
result_text.grid(row=4, column=1, padx=5, pady=5)


root.mainloop()