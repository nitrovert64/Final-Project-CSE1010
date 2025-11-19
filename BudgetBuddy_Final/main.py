import os
from library import functions
from library.expense_tracker import ExpenseTracker

os.system("cls" if os.name == "nt" else "clear")

name = input("Enter your name: ")
os.system("cls" if os.name == "nt" else "clear")
print(f"Hi {name}, this is BudgetBuddy! Your personal budgeting assistant.")

income = float(input("Enter your monthly income (numbers only): "))



budget_tracker = ExpenseTracker()      
budget_tracker.add_expenses()





total_expenses = budget_tracker.get_expenses_details()

functions.print_summary(income, total_expenses)