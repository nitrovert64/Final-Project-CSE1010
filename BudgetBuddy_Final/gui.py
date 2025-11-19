import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from library.expense_tracker import ExpenseTracker

class BudgetGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("BudgetBuddy")
        self.root.geometry("500x650")

        # -------------------- COLOR PALETTE --------------------
        self.bg_main = "#F8F9FA"
        self.bg_card = "#E0E0E0"
        self.fg_text = "#424242"
        self.btn_bg = "#4CAF50"
        self.btn_fg = "#FFFFFF"
        self.border = "#9E9E9E"
        self.hover_bg = "#A8D5BA"
        self.bar_fill = "#4CAF50"
        self.bar_trough = "#E0E0E0"

        self.root.configure(bg=self.bg_main)
        self.tracker = ExpenseTracker()
        self.income = 0
        self.font = ("Segoe UI", 11)

        # -------------------- TITLE --------------------
        title = tk.Label(
            root, text="BudgetBuddy",
            font=("Segoe UI", 22, "bold"),
            bg=self.bg_main, fg=self.fg_text
        )
        title.pack(pady=15)

        # -------------------- INCOME SECTION --------------------
        income_frame = tk.Frame(root, bg=self.bg_card, padx=15, pady=15, highlightbackground=self.border, highlightthickness=1)
        income_frame.pack(pady=10)

        tk.Label(income_frame, text="Monthly Income:", font=self.font, bg=self.bg_card, fg=self.fg_text)\
            .grid(row=0, column=0, pady=5)
        self.income_entry = tk.Entry(income_frame, width=20, font=self.font)
        self.income_entry.grid(row=0, column=1, padx=10)

        btn_income = tk.Button(
            income_frame, text="Set Income", command=self.set_income,
            bg=self.btn_bg, fg=self.btn_fg, font=self.font, padx=10, pady=5
        )
        btn_income.grid(row=0, column=2, padx=5)
        self.add_hover(btn_income)

        # -------------------- EXPENSE INPUT --------------------
        expense_frame = tk.Frame(root, bg=self.bg_card, padx=15, pady=15, highlightbackground=self.border, highlightthickness=1)
        expense_frame.pack(pady=10)

        tk.Label(expense_frame, text="Category:", bg=self.bg_card, fg=self.fg_text, font=self.font)\
            .grid(row=1, column=0, pady=5)
        self.category_entry = tk.Entry(expense_frame, width=20, font=self.font)
        self.category_entry.grid(row=1, column=1)

        tk.Label(expense_frame, text="Amount:", bg=self.bg_card, fg=self.fg_text, font=self.font)\
            .grid(row=2, column=0, pady=5)
        self.amount_entry = tk.Entry(expense_frame, width=20, font=self.font)
        self.amount_entry.grid(row=2, column=1)

        btn_expense = tk.Button(
            expense_frame, text="Add Expense", command=self.add_expense,
            bg=self.btn_bg, fg=self.btn_fg, font=self.font, padx=15, pady=5
        )
        btn_expense.grid(row=3, column=1, pady=10)
        self.add_hover(btn_expense)

        # -------------------- TEXT OUTPUT --------------------
        self.output = tk.Text(root, height=15, width=50, font=("Consolas", 11),
                              bg=self.bg_card, fg=self.fg_text, insertbackground=self.fg_text)
        self.output.pack(pady=10)

        # -------------------- PROGRESS BAR --------------------
        bar_frame = tk.Frame(root, bg=self.bg_main)
        bar_frame.pack(pady=5)

        tk.Label(bar_frame, text="Remaining Budget:", font=self.font, bg=self.bg_main, fg=self.fg_text)\
            .pack()

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("green.Horizontal.TProgressbar",
                        background=self.bar_fill, troughcolor=self.bar_trough, thickness=20)

        self.progress = ttk.Progressbar(
            bar_frame, length=300, style="green.Horizontal.TProgressbar"
        )
        self.progress.pack(pady=5)

        # -------------------- ACTION BUTTONS --------------------
        button_frame = tk.Frame(root, bg=self.bg_main)
        button_frame.pack(pady=15)

        btn_save = tk.Button(
            button_frame, text="Save to File", command=self.save_to_file,
            bg=self.btn_bg, fg=self.btn_fg, font=self.font, padx=20, pady=7
        )
        btn_save.grid(row=0, column=0, padx=10)
        self.add_hover(btn_save)

        btn_chart = tk.Button(
            button_frame, text="Show Pie Chart", command=self.show_chart,
            bg=self.btn_bg, fg=self.btn_fg, font=self.font, padx=20, pady=7
        )
        btn_chart.grid(row=0, column=1, padx=10)
        self.add_hover(btn_chart)

    # -------------------- FUNCTIONS --------------------

    def add_hover(self, widget):
        widget.bind("<Enter>", lambda e: widget.config(bg=self.hover_bg))
        widget.bind("<Leave>", lambda e: widget.config(bg=self.btn_bg))

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
