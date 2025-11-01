import tkinter as tk
from tkinter import ttk, messagebox
from itertools import permutations
class GraphTableSolver:
    def __init__(self, root):
        self.root = root
        self.root.geometry("900x700")
        self.current_step = 0
        self.nodes = []
        self.table_data = {}
        self.graph_data = {}
        self.entries = {}
        self.solution = None
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.content_frame = tk.Frame(self.main_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        self.button_frame = tk.Frame(self.main_frame, pady=10)
        self.button_frame.pack(fill=tk.X, side=tk.BOTTOM)
        self.back_btn = tk.Button(self.button_frame, text="← Назад", command=self.prev_step,
                                   font=("Arial", 11), padx=20, pady=5, state=tk.DISABLED)
        self.back_btn.pack(side=tk.LEFT, padx=20)
        self.next_btn = tk.Button(self.button_frame, text="Далее →", command=self.next_step,
                                   font=("Arial", 11), bg="#2196F3", fg="white", padx=20, pady=5)
        self.next_btn.pack(side=tk.RIGHT, padx=20)
        self.show_step()
    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    def update_buttons(self):
        if self.current_step == 0:
            self.back_btn.config(state=tk.DISABLED)
            self.next_btn.config(text="Далее →", state=tk.NORMAL)
        elif self.current_step == 2:
            self.back_btn.config(state=tk.NORMAL)
            self.next_btn.config(text="Решить", state=tk.NORMAL)
        elif self.current_step == 3:
            self.back_btn.config(state=tk.NORMAL)
            self.next_btn.config(text="Новая задача", state=tk.NORMAL)
        else:
            self.back_btn.config(state=tk.NORMAL)
            self.next_btn.config(text="Далее →", state=tk.NORMAL)
    def show_step(self):
        self.clear_content()
        if self.current_step == 0:
            self.show_step_nodes()
        elif self.current_step == 1:
            self.show_step_table()
        elif self.current_step == 2:
            self.show_step_graph()
        elif self.current_step == 3:
            self.show_step_result()
        self.update_buttons()
    def next_step(self):
        if self.current_step == 0:
            if not self.validate_nodes():
                return
        elif self.current_step == 1:
            if not self.save_table():
                return
        elif self.current_step == 2:
            if not self.save_graph():
                return
            if not self.solve():
                return
        elif self.current_step == 3:
            self.current_step = -1
            self.nodes = []
            self.table_data = {}
            self.graph_data = {}
            self.entries = {}
            self.solution = None
        self.current_step += 1
        self.show_step()
    def prev_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.show_step()
    def show_step_nodes(self):
        frame = tk.Frame(self.content_frame)
        frame.pack(expand=True)
        tk.Label(frame, text="Шаг 1 из 3", font=("Arial", 10), fg="#666").pack(pady=5)
        tk.Label(frame, text="Введите количество вершин", font=("Arial", 16, "bold")).pack(pady=20)
        self.nodes_entry = tk.Entry(frame, font=("Arial", 14), width=10, justify='center')
        self.nodes_entry.pack(pady=10)
        self.nodes_entry.focus()
        self.nodes_entry.bind('<Return>', lambda e: self.next_step())
        if self.nodes:
            self.nodes_entry.insert(0, str(len(self.nodes)))
        tk.Label(frame, text="Количество населенных пунктов в задаче (2-10)", 
                font=("Arial", 10), fg="#666").pack(pady=5)
    def validate_nodes(self):
        try:
            n = int(self.nodes_entry.get())
            if n < 2 or n > 10:
                messagebox.showerror("Ошибка", "Количество вершин должно быть от 2 до 10")
                return False
            self.nodes = list(range(1, n + 1))
            return True
        except ValueError:
            messagebox.showerror("Ошибка", "Введите целое число")
            return False
    def show_step_table(self):
        header = tk.Frame(self.content_frame, bg="#f0f0f0", pady=10)
        header.pack(fill=tk.X)
        tk.Label(header, text="Шаг 2 из 3", font=("Arial", 10), fg="#666", bg="#f0f0f0").pack()
        tk.Label(header, text="Заполните таблицу смежности", 
                font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=5)
        tk.Label(header, text="Введите длины дорог из таблицы задачи", 
                font=("Arial", 10), fg="#666", bg="#f0f0f0").pack()
        table_frame = tk.Frame(self.content_frame)
        table_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)
        canvas = tk.Canvas(table_frame)
        scrollbar_y = ttk.Scrollbar(table_frame, orient="vertical", command=canvas.yview)
        scrollbar_x = ttk.Scrollbar(table_frame, orient="horizontal", command=canvas.xview)
        scrollable_frame = tk.Frame(canvas)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        n = len(self.nodes)
        tk.Label(scrollable_frame, text="", width=5, height=2, relief=tk.RIDGE).grid(row=0, column=0)
        for i, node in enumerate(self.nodes):
            tk.Label(scrollable_frame, text=str(node), width=8, height=2, 
                    relief=tk.RIDGE, font=("Arial", 10, "bold"), bg="#e0e0e0").grid(row=0, column=i+1)
        self.entries = {}
        for i, row_node in enumerate(self.nodes):
            tk.Label(scrollable_frame, text=str(row_node), width=5, height=2, 
                    relief=tk.RIDGE, font=("Arial", 10, "bold"), bg="#e0e0e0").grid(row=i+1, column=0)
            for j, col_node in enumerate(self.nodes):
                if i >= j:
                    tk.Label(scrollable_frame, text="", width=8, height=2, 
                            relief=tk.RIDGE, bg="#808080").grid(row=i+1, column=j+1)
                else:
                    entry = tk.Entry(scrollable_frame, width=8, font=("Arial", 10), justify='center')
                    entry.grid(row=i+1, column=j+1, padx=1, pady=1)
                    self.entries[(row_node, col_node)] = entry
                    if self.table_data and str(row_node) in self.table_data and str(col_node) in self.table_data[str(row_node)]:
                        entry.insert(0, str(self.table_data[str(row_node)][str(col_node)]))
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")
    def save_table(self):
        self.table_data = {}
        for (i, j), entry in self.entries.items():
            value = entry.get().strip()
            if value:
                try:
                    length = int(value)
                    if str(i) not in self.table_data:
                        self.table_data[str(i)] = {}
                    if str(j) not in self.table_data:
                        self.table_data[str(j)] = {}
                    self.table_data[str(i)][str(j)] = length
                    self.table_data[str(j)][str(i)] = length
                except ValueError:
                    messagebox.showerror("Ошибка", f"Некорректное значение в ячейке ({i}, {j})")
                    return False
        if not self.table_data:
            messagebox.showerror("Ошибка", "Заполните хотя бы одну связь")
            return False
        return True
    def show_step_graph(self):
        header = tk.Frame(self.content_frame, bg="#f0f0f0", pady=10)
        header.pack(fill=tk.X)
        tk.Label(header, text="Шаг 3 из 3", font=("Arial", 10), fg="#666", bg="#f0f0f0").pack()
        tk.Label(header, text="Введите структуру графа", 
                font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=5)
        tk.Label(header, text="Укажите вершины и их соседей (например: для А соседи БВ)", 
                font=("Arial", 10), fg="#666", bg="#f0f0f0").pack()
        graph_frame = tk.Frame(self.content_frame)
        graph_frame.pack(expand=True, pady=20)
        tk.Label(graph_frame, text="Вершина", font=("Arial", 11, "bold")).grid(row=0, column=0, padx=10, pady=5)
        tk.Label(graph_frame, text="Соседние вершины", font=("Arial", 11, "bold")).grid(row=0, column=1, padx=10, pady=5)
        self.graph_entries = {}
        for i in range(len(self.nodes)):
            node_entry = tk.Entry(graph_frame, width=8, font=("Arial", 11), justify='center')
            node_entry.grid(row=i+1, column=0, padx=10, pady=3)
            neighbors_entry = tk.Entry(graph_frame, width=30, font=("Arial", 11))
            neighbors_entry.grid(row=i+1, column=1, padx=10, pady=3)
            if self.graph_data:
                items = list(self.graph_data.items())
                if i < len(items):
                    node_entry.insert(0, items[i][0])
                    neighbors_entry.insert(0, items[i][1])
            self.graph_entries[i] = (node_entry, neighbors_entry)
    def save_graph(self):
        self.graph_data = {}
        for i, (node_entry, neighbors_entry) in self.graph_entries.items():
            node = node_entry.get().strip().upper()
            neighbors = neighbors_entry.get().strip().upper().replace(',', '').replace(' ', '')
            if node and neighbors:
                self.graph_data[node] = neighbors
        if not self.graph_data:
            messagebox.showerror("Ошибка", "Введите данные графа")
            return False
        return True
    def show_step_solve(self):
        header = tk.Frame(self.content_frame, bg="#f0f0f0", pady=10)
        header.pack(fill=tk.X)
        tk.Label(header, text="Шаг 4 из 4", font=("Arial", 10), fg="#666", bg="#f0f0f0").pack()
        tk.Label(header, text="Проверьте данные", 
                font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=5)
        main = tk.Frame(self.content_frame)
        main.pack(expand=True, fill=tk.BOTH, padx=40, pady=20)
        left = tk.LabelFrame(main, text="Таблица смежности", font=("Arial", 11, "bold"), padx=10, pady=10)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        canvas_table = tk.Canvas(left, height=300)
        scroll_table = ttk.Scrollbar(left, orient="vertical", command=canvas_table.yview)
        frame_table = tk.Frame(canvas_table)
        frame_table.bind("<Configure>", lambda e: canvas_table.configure(scrollregion=canvas_table.bbox("all")))
        canvas_table.create_window((0, 0), window=frame_table, anchor="nw")
        canvas_table.configure(yscrollcommand=scroll_table.set)
        for node1 in sorted(self.table_data.keys()):
            for node2 in sorted(self.table_data[node1].keys()):
                if int(node1) < int(node2):
                    tk.Label(frame_table, text=f"{node1} ↔ {node2}: {self.table_data[node1][node2]}", 
                            font=("Arial", 10), anchor='w').pack(fill=tk.X, padx=5, pady=2)
        canvas_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_table.pack(side=tk.RIGHT, fill=tk.Y)
        right = tk.LabelFrame(main, text="Структура графа", font=("Arial", 11, "bold"), padx=10, pady=10)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)
        canvas_graph = tk.Canvas(right, height=300)
        scroll_graph = ttk.Scrollbar(right, orient="vertical", command=canvas_graph.yview)
        frame_graph = tk.Frame(canvas_graph)
        frame_graph.bind("<Configure>", lambda e: canvas_graph.configure(scrollregion=canvas_graph.bbox("all")))
        canvas_graph.create_window((0, 0), window=frame_graph, anchor="nw")
        canvas_graph.configure(yscrollcommand=scroll_graph.set)
        for node, neighbors in sorted(self.graph_data.items()):
            tk.Label(frame_graph, text=f"{node}: {neighbors}", 
                    font=("Arial", 10), anchor='w').pack(fill=tk.X, padx=5, pady=2)
        canvas_graph.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_graph.pack(side=tk.RIGHT, fill=tk.Y)
        info = tk.Frame(self.content_frame)
        info.pack(pady=10)
        tk.Label(info, text="Нажмите 'Решить' для поиска соответствия", 
                font=("Arial", 11), fg="#666").pack()
    def solve(self):
        table_adj = {}
        for node in self.table_data:
            table_adj[node] = ''.join(sorted(self.table_data[node].keys()))
        graph_sorted = {k: ''.join(sorted(v)) for k, v in sorted(self.graph_data.items())}
        nodes_list = list(self.table_data.keys())
        graph_nodes = list(self.graph_data.keys())
        self.solution = None
        for perm in permutations(nodes_list):
            mapping = {num: letter for num, letter in zip(perm, graph_nodes)}
            mapped_table = {}
            for num, neighbors in table_adj.items():
                if num in mapping:
                    mapped_neighbors = ''.join(sorted([mapping[n] for n in neighbors if n in mapping]))
                    mapped_table[mapping[num]] = mapped_neighbors
            if mapped_table == graph_sorted:
                self.solution = mapping
                break
        if not self.solution:
            messagebox.showerror("Ошибка", "Не удалось найти соответствие.\nПроверьте правильность данных.")
            return False
        return True
    def show_step_result(self):
        header = tk.Frame(self.content_frame, bg="#f0f0f0", pady=15)
        header.pack(fill=tk.X)
        tk.Label(header, text="✓ Решение найдено!", 
                font=("Arial", 16, "bold"), fg="#4CAF50", bg="#f0f0f0").pack()
        main = tk.Frame(self.content_frame)
        main.pack(expand=True, fill=tk.BOTH, padx=40, pady=20)
        left = tk.LabelFrame(main, text="Соответствие номеров и вершин", font=("Arial", 11, "bold"), padx=20, pady=15)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        result_frame = tk.Frame(left)
        result_frame.pack()
        tk.Label(result_frame, text="Номер", font=("Arial", 11, "bold"), width=10, 
                relief=tk.RIDGE, bg="#e0e0e0").grid(row=0, column=0)
        tk.Label(result_frame, text="Вершина", font=("Arial", 11, "bold"), width=10, 
                relief=tk.RIDGE, bg="#e0e0e0").grid(row=0, column=1)
        for i, (num, letter) in enumerate(sorted(self.solution.items()), start=1):
            tk.Label(result_frame, text=num, font=("Arial", 10), width=10, 
                    relief=tk.RIDGE).grid(row=i, column=0)
            tk.Label(result_frame, text=letter, font=("Arial", 10), width=10, 
                    relief=tk.RIDGE).grid(row=i, column=1)
        right = tk.LabelFrame(main, text="Найти расстояние", font=("Arial", 11, "bold"), padx=20, pady=15)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)
        calc_frame = tk.Frame(right)
        calc_frame.pack(expand=True)
        input_frame = tk.Frame(calc_frame)
        input_frame.pack(pady=10)
        tk.Label(input_frame, text="Из:", font=("Arial", 11)).grid(row=0, column=0, padx=5)
        from_entry = tk.Entry(input_frame, width=5, font=("Arial", 12), justify='center')
        from_entry.grid(row=0, column=1, padx=5)
        tk.Label(input_frame, text="В:", font=("Arial", 11)).grid(row=0, column=2, padx=5)
        to_entry = tk.Entry(input_frame, width=5, font=("Arial", 12), justify='center')
        to_entry.grid(row=0, column=3, padx=5)
        result_label = tk.Label(calc_frame, text="", font=("Arial", 14, "bold"), fg="#2196F3")
        result_label.pack(pady=15)
        def calculate_distance():
            from_node = from_entry.get().strip().upper()
            to_node = to_entry.get().strip().upper()
            reverse_map = {v: k for k, v in self.solution.items()}
            if from_node not in reverse_map or to_node not in reverse_map:
                result_label.config(text="Вершины не найдены", fg="red")
                return
            num1 = reverse_map[from_node]
            num2 = reverse_map[to_node]
            if num1 in self.table_data and num2 in self.table_data[num1]:
                distance = self.table_data[num1][num2]
                result_label.config(text=f"Расстояние: {distance}", fg="#4CAF50")
            else:
                result_label.config(text="Дорога не найдена", fg="red")
        tk.Button(calc_frame, text="Найти", command=calculate_distance,
                 font=("Arial", 11), bg="#2196F3", fg="white", padx=25, pady=5).pack()
if __name__ == "__main__":
    root = tk.Tk()
    app = GraphTableSolver(root)
    root.mainloop()