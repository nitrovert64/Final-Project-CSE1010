import tkinter as tk
from tkinter import messagebox
from library.expense_tracker import ExpenseTracker

class BudgetGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("BudgetBuddy")

        # Use your ExpenseTracker class
        self.tracker = ExpenseTracker()

        # Store income
        self.income = 0

        # Income section
        tk.Label(root, text="Monthly Income:").grid(row=0, column=0, padx=5, pady=5)
        self.income_entry = tk.Entry(root)
        self.income_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Button(root, text="Set Income", command=self.set_income).grid(row=0, column=2, padx=5)

        # Expense inputs
        tk.Label(root, text="Category:").grid(row=1, column=0, padx=5)
        self.category_entry = tk.Entry(root)
        self.category_entry.grid(row=1, column=1, padx=5)

        tk.Label(root, text="Amount:").grid(row=2, column=0, padx=5)
        self.amount_entry = tk.Entry(root)
        self.amount_entry.grid(row=2, column=1, padx=5)

        tk.Button(root, text="Add Expense", command=self.add_expense).grid(row=3, column=1, pady=5)

        # Expense display
        self.output = tk.Text(root, height=12, width=40)
        self.output.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

        # Save button
        tk.Button(root, text="Save to File", command=self.save_to_file).grid(row=5, column=1, pady=5)

    # -------------------- GUI FUNCTIONALITY --------------------

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

        if category == "" or amount_text == "":
            messagebox.showerror("Error", "Both fields required")
            return

        try:
            amount = float(amount_text)
        except:
            messagebox.showerror("Error", "Enter a valid number for amount")
            return

        # Add the expense using your class
        self.tracker.expenses[category] = amount

        # Update the display
        self.update_display()

        # Clear inputs
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

        total_expenses = 0

        self.output.insert(tk.END, "Expenses:\n")
        for cat, amt in self.tracker.expenses.items():
            self.output.insert(tk.END, f"{cat}: ${amt:.2f}\n")
            total_expenses += amt

        balance = self.income - total_expenses

        self.output.insert(tk.END, "\n")
        self.output.insert(tk.END, f"Total Expenses: ${total_expenses:.2f}\n")
        self.output.insert(tk.END, f"Remaining Balance: ${balance:.2f}\n")


# -------------------- RUN GUI --------------------
root = tk.Tk()
app = BudgetGUI(root)
root.mainloop()
