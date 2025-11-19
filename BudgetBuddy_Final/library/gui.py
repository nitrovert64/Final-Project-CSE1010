import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from library.expense_tracker import ExpenseTracker

class BudgetGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("BudgetBuddy")
        self.root.geometry("500x650")
        self.root.configure(bg="#1E1E2E")  # dark purple charcoal

        self.tracker = ExpenseTracker()
        self.income = 0

        # Universal Font
        self.font = ("Segoe UI", 11)

        # -------------------- TITLE --------------------
        title = tk.Label(
            root, text="BudgetBuddy",
            font=("Segoe UI", 22, "bold"),
            bg="#1E1E2E", fg="white"
        )
        title.pack(pady=15)

        # -------------------- INCOME SECTION --------------------
        income_frame = tk.Frame(root, bg="#2A2A3B", padx=15, pady=15)
        income_frame.pack(pady=10)

        tk.Label(income_frame, text="Monthly Income:", font=self.font, bg="#2A2A3B", fg="white")\
            .grid(row=0, column=0, pady=5)
        self.income_entry = tk.Entry(income_frame, width=20, font=self.font)
        self.income_entry.grid(row=0, column=1, padx=10)

        tk.Button(
            income_frame, text="Set Income", command=self.set_income,
            bg="#9D4EDD", fg="white", font=self.font, padx=10, pady=5
        ).grid(row=0, column=2, padx=5)

        # -------------------- EXPENSE INPUT --------------------
        expense_frame = tk.Frame(root, bg="#2A2A3B", padx=15, pady=15)
        expense_frame.pack(pady=10)

        tk.Label(expense_frame, text="Category:", bg="#2A2A3B", fg="white", font=self.font)\
            .grid(row=1, column=0, pady=5)
        self.category_entry = tk.Entry(expense_frame, width=20, font=self.font)
        self.category_entry.grid(row=1, column=1)

        tk.Label(expense_frame, text="Amount:", bg="#2A2A3B", fg="white", font=self.font)\
            .grid(row=2, column=0, pady=5)
        self.amount_entry = tk.Entry(expense_frame, width=20, font=self.font)
        self.amount_entry.grid(row=2, column=1)

        tk.Button(
            expense_frame, text="Add Expense", command=self.add_expense,
            bg="#7B2CBF", fg="white", font=self.font, padx=15, pady=5
        ).grid(row=3, column=1, pady=10)

        # -------------------- TEXT OUTPUT --------------------
        self.output = tk.Text(root, height=15, width=50, font=("Consolas", 11),
                              bg="#2A2A3B", fg="white", insertbackground="white")
        self.output.pack(pady=10)

        # -------------------- PROGRESS BAR --------------------
        bar_frame = tk.Frame(root, bg="#1E1E2E")
        bar_frame.pack(pady=5)

        tk.Label(bar_frame, text="Remaining Budget:", font=self.font, bg="#1E1E2E", fg="white")\
            .pack()

        # Style the progress bar
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("purple.Horizontal.TProgressbar",
                        background="#9D4EDD", troughcolor="#2A2A3B", thickness=20)

        self.progress = ttk.Progressbar(
            bar_frame, length=300, style="purple.Horizontal.TProgressbar"
        )
        self.progress.pack(pady=5)

        # -------------------- ACTION BUTTONS --------------------
        button_frame = tk.Frame(root, bg="#1E1E2E")
        button_frame.pack(pady=15)

        tk.Button(
            button_frame, text="Save to File", command=self.save_to_file,
            bg="#9D4EDD", fg="white", font=self.font, padx=20, pady=7
        ).grid(row=0, column=0, padx=10)

        tk.Button(
            button_frame, text="Show Pie Chart", command=self.show_chart,
            bg="#7B2CBF", fg="white", font=self.font, padx=20, pady=7
        ).grid(row=0, column=1, padx=10)

    # -------------------- FUNCTIONS --------------------

    def set_income(self):
        try:
            self.income = float(self.income_entry.get())
            messagebox.showinfo("Success", "Income saved!")
            self.update_display()
        except:
            messagebox.showerror("Error", "Enter a valid number")

    def add_expense(self):
        category = self.category_entry.get()
        amount_text = self.amount_entry.get()

        if not category or not amount_text:
            messagebox.showerror("Error", "Both fields required")
            return

        try:
            amount = float(amount_text)
        except:
            messagebox.showerror("Error", "Amount must be a number")
            return

        self.tracker.expenses[category] = amount
        self.update_display()

        self.category_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)

    def save_to_file(self):
        if not self.tracker.expenses:
            messagebox.showerror("Error", "No expenses to save")
            return

        self.tracker.write_to_file(self.tracker.expenses)
        messagebox.showinfo("Saved", "Expenses saved to expenses.txt")

    def update_display(self):
        self.output.delete("1.0", tk.END)

        total = 0

        self.output.insert(tk.END, "Expenses:\n")
        for cat, amt in self.tracker.expenses.items():
            self.output.insert(tk.END, f"{cat:<15} ${amt:.2f}\n")
            total += amt

        balance = self.income - total

        self.output.insert(tk.END, f"\nTotal Expenses:  ${total:.2f}\n")
        self.output.insert(tk.END, f"Remaining:       ${balance:.2f}\n")

        # Update progress bar
        if self.income > 0:
            used_percent = min((total / self.income) * 100, 100)
            self.progress["value"] = 100 - used_percent

    def show_chart(self):
        if not self.tracker.expenses:
            messagebox.showerror("Error", "No expenses to show")
            return

        labels = list(self.tracker.expenses.keys())
        sizes = list(self.tracker.expenses.values())

        plt.figure(figsize=(6, 6))
        plt.pie(sizes, labels=labels, autopct="%1.1f%%")
        plt.title("Expense Breakdown")
        plt.show()


# -------------------- RUN GUI --------------------
root = tk.Tk()
app = BudgetGUI(root)
root.mainloop()
