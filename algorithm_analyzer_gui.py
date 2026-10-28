
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import random
import time
import csv
import math

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# ---------------- SORTING ALGORITHMS ----------------

def bubble_sort(arr):
    arr = arr.copy()
    n = len(arr)

    for i in range(n):
        swapped = False

        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True

        if not swapped:
            break

    return arr


def merge_sort(arr):
    if len(arr) <= 1:
        return arr.copy()

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


def quick_sort(arr):
    arr = arr.copy()

    def sort(low, high):
        if low >= high:
            return

        pivot_index = random.randint(low, high)
        arr[pivot_index], arr[high] = arr[high], arr[pivot_index]
        pivot = arr[high]

        i = low - 1

        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]

        i += 1
        arr[i], arr[high] = arr[high], arr[i]

        sort(low, i - 1)
        sort(i + 1, high)

    sort(0, len(arr) - 1)
    return arr


# ---------------- SEARCHING ALGORITHMS ----------------

def linear_search(arr, target):
    for i, value in enumerate(arr):
        if value == target:
            return i
    return -1


def binary_search(arr, target):
    low = 0
    high = len(arr) - 1

    while low <= high:
        mid = (low + high) // 2

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return -1


# ---------------- MAIN APPLICATION ----------------

class AlgorithmAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("Algorithm Performance Analyzer")
        self.root.geometry("1100x720")
        self.root.minsize(850, 600)

        self.results = []
        self.status = tk.StringVar(value="Ready to analyze algorithms.")

        self.create_widgets()

    def create_widgets(self):
        header = tk.Frame(self.root, bg="#17365D", pady=16)
        header.pack(fill="x")

        tk.Label(
            header,
            text="ALGORITHM PERFORMANCE ANALYZER",
            font=("Arial", 20, "bold"),
            bg="#17365D",
            fg="white"
        ).pack()

        tk.Label(
            header,
            text="Design and Analysis of Algorithms | Python Project",
            font=("Arial", 10),
            bg="#17365D",
            fg="#DCE6F1"
        ).pack(pady=(5, 0))

        controls = ttk.Frame(self.root, padding=12)
        controls.pack(fill="x")

        ttk.Button(
            controls,
            text="Analyze Sorting",
            command=self.analyze_sorting
        ).pack(side="left", padx=5)

        ttk.Button(
            controls,
            text="Analyze Searching",
            command=self.analyze_searching
        ).pack(side="left", padx=5)

        ttk.Button(
            controls,
            text="Complexity Table",
            command=self.show_complexities
        ).pack(side="left", padx=5)

        ttk.Button(
            controls,
            text="Export CSV",
            command=self.export_csv
        ).pack(side="left", padx=5)

        ttk.Button(
            controls,
            text="Clear Results",
            command=self.clear_results
        ).pack(side="left", padx=5)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=12, pady=5)

        self.graph_tab = ttk.Frame(self.notebook)
        self.table_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.graph_tab, text="Performance Graph")
        self.notebook.add(self.table_tab, text="Results Table")

        self.figure = Figure(figsize=(8, 4.5), dpi=100)
        self.axis = self.figure.add_subplot(111)
        self.axis.set_title("Run an analysis to display a graph")
        self.axis.set_xlabel("Input Size")
        self.axis.set_ylabel("Execution Time (milliseconds)")
        self.figure.tight_layout()

        self.canvas = FigureCanvasTkAgg(
            self.figure,
            master=self.graph_tab
        )
        self.canvas.get_tk_widget().pack(
            fill="both", expand=True, padx=8, pady=8
        )
        self.canvas.draw()

        columns = ("category", "algorithm", "size", "time")
        self.tree = ttk.Treeview(
            self.table_tab,
            columns=columns,
            show="headings"
        )

        self.tree.heading("category", text="Category")
        self.tree.heading("algorithm", text="Algorithm")
        self.tree.heading("size", text="Input Size")
        self.tree.heading("time", text="Time (ms)")

        self.tree.column("category", width=140, anchor="center")
        self.tree.column("algorithm", width=180, anchor="center")
        self.tree.column("size", width=120, anchor="center")
        self.tree.column("time", width=150, anchor="center")

        scrollbar = ttk.Scrollbar(
            self.table_tab,
            orient="vertical",
            command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(
            side="left", fill="both", expand=True, padx=(8, 0), pady=8
        )
        scrollbar.pack(side="right", fill="y", padx=(0, 8), pady=8)

        ttk.Label(
            self.root,
            textvariable=self.status,
            relief="sunken",
            anchor="w",
            padding=6
        ).pack(fill="x", side="bottom")

    # ---------------- PERFORMANCE TESTING ----------------

    def measure_time(self, function, data):
        start = time.perf_counter()
        output = function(data)
        elapsed = (time.perf_counter() - start) * 1000
        return elapsed, output

    def analyze_sorting(self):
        self.status.set("Analyzing sorting algorithms...")
        self.root.update_idletasks()

        sizes = [100, 300, 500, 1000, 2000]
        algorithms = {
            "Bubble Sort": bubble_sort,
            "Merge Sort": merge_sort,
            "Quick Sort": quick_sort
        }

        local_results = []

        try:
            for size in sizes:
                data = [random.randint(0, 10000) for _ in range(size)]

                for name, function in algorithms.items():
                    elapsed, output = self.measure_time(function, data)

                    if output != sorted(data):
                        raise ValueError(name + " produced an incorrect result.")

                    local_results.append({
                        "category": "Sorting",
                        "algorithm": name,
                        "size": size,
                        "time": elapsed
                    })

            self.results = [
                r for r in self.results if r["category"] != "Sorting"
            ] + local_results

            self.refresh_table()
            self.draw_graph(local_results, "Sorting Algorithm Comparison")
            self.status.set("Sorting analysis completed successfully.")

        except Exception as error:
            messagebox.showerror("Analysis Error", str(error))
            self.status.set("Sorting analysis failed.")

    def analyze_searching(self):
        self.status.set("Analyzing searching algorithms...")
        self.root.update_idletasks()

        sizes = [1000, 5000, 10000, 50000, 100000]
        algorithms = {
            "Linear Search": linear_search,
            "Binary Search": binary_search
        }

        local_results = []

        for size in sizes:
            data = list(range(size))
            target = size - 1

            for name, function in algorithms.items():
                total = 0
                trials = 10

                for _ in range(trials):
                    start = time.perf_counter()
                    result = function(data, target)
                    total += time.perf_counter() - start

                    if result != target:
                        messagebox.showerror(
                            "Validation Error",
                            name + " did not find the expected element."
                        )
                        self.status.set("Searching analysis failed.")
                        return

                average_ms = (total / trials) * 1000

                local_results.append({
                    "category": "Searching",
                    "algorithm": name,
                    "size": size,
                    "time": average_ms
                })

        self.results = [
            r for r in self.results if r["category"] != "Searching"
        ] + local_results

        self.refresh_table()
        self.draw_graph(local_results, "Searching Algorithm Comparison")
        self.status.set("Searching analysis completed successfully.")

    # ---------------- GRAPH VISUALIZATION ----------------

    def draw_graph(self, data, title):
        self.axis.clear()

        algorithms = sorted(set(r["algorithm"] for r in data))

        for algorithm in algorithms:
            points = [
                r for r in data if r["algorithm"] == algorithm
            ]
            points.sort(key=lambda r: r["size"])

            x_values = [r["size"] for r in points]
            y_values = [r["time"] for r in points]

            self.axis.plot(
                x_values,
                y_values,
                marker="o",
                linewidth=2,
                label=algorithm
            )

        self.axis.set_title(title)
        self.axis.set_xlabel("Input Size (n)")
        self.axis.set_ylabel("Average Execution Time (ms)")
        self.axis.grid(True, linestyle="--", alpha=0.5)
        self.axis.legend()
        self.figure.tight_layout()
        self.canvas.draw()

        self.notebook.select(self.graph_tab)

        safe_title = (
            "sorting_comparison.png"
            if "Sorting" in title
            else "searching_comparison.png"
        )

        try:
            self.figure.savefig(safe_title, dpi=150)
        except OSError:
            pass

    # ---------------- RESULTS TABLE ----------------

    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for result in self.results:
            self.tree.insert(
                "",
                "end",
                values=(
                    result["category"],
                    result["algorithm"],
                    result["size"],
                    f'{result["time"]:.6f}'
                )
            )

    # ---------------- COMPLEXITY TABLE ----------------

    def show_complexities(self):
        window = tk.Toplevel(self.root)
        window.title("Algorithm Time Complexities")
        window.geometry("800x330")

        columns = ("algorithm", "best", "average", "worst")
        tree = ttk.Treeview(
            window,
            columns=columns,
            show="headings"
        )

        headings = {
            "algorithm": "Algorithm",
            "best": "Best Case",
            "average": "Average Case",
            "worst": "Worst Case"
        }

        for col, heading in headings.items():
            tree.heading(col, text=heading)
            tree.column(col, width=180, anchor="center")

        rows = [
            ("Bubble Sort", "O(n)", "O(n²)", "O(n²)"),
            ("Merge Sort", "O(n log n)", "O(n log n)", "O(n log n)"),
            ("Quick Sort", "O(n log n)", "O(n log n)", "O(n²)"),
            ("Linear Search", "O(1)", "O(n)", "O(n)"),
            ("Binary Search", "O(1)", "O(log n)", "O(log n)")
        ]

        for row in rows:
            tree.insert("", "end", values=row)

        tree.pack(fill="both", expand=True, padx=12, pady=12)

        ttk.Label(
            window,
            text="Note: Binary Search requires sorted input data.",
            padding=8
        ).pack()

    # ---------------- CSV EXPORT ----------------

    def export_csv(self):
        if not self.results:
            messagebox.showinfo(
                "No Results",
                "Run a sorting or searching analysis first."
            )
            return

        filename = filedialog.asksaveasfilename(
            title="Save Analysis Results",
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")],
            initialfile="algorithm_results.csv"
        )

        if not filename:
            return

        try:
            with open(filename, "w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(
                    file,
                    fieldnames=["category", "algorithm", "size", "time"]
                )
                writer.writeheader()
                writer.writerows(self.results)

            messagebox.showinfo(
                "Export Successful",
                "Results saved to:\n" + filename
            )
            self.status.set("CSV results exported successfully.")

        except OSError as error:
            messagebox.showerror("Export Error", str(error))

    # ---------------- RESET ----------------

    def clear_results(self):
        self.results.clear()
        self.refresh_table()
        self.axis.clear()
        self.axis.set_title("Run an analysis to display a graph")
        self.axis.set_xlabel("Input Size")
        self.axis.set_ylabel("Execution Time (milliseconds)")
        self.figure.tight_layout()
        self.canvas.draw()
        self.status.set("Results cleared.")


# ---------------- RUN APPLICATION ----------------

if __name__ == "__main__":
    root = tk.Tk()
    app = AlgorithmAnalyzer(root)
    root.mainloop()
