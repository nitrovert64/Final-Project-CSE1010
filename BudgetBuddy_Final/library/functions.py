# library/functions.py

def print_summary(income, total_expenses):
    balance = income - total_expenses

    print("\n--- SUMMARY ---")
    print(f"Total monthly income: ${income}")
    print(f"Total expenses: ${total_expenses}")
    print(f"Remaining balance: ${balance}")

    if balance > 0:
        print("Great! You are saving money!")
    elif balance == 0:
        print("You are breaking even.")
    else:
        print("**WARNING** You are overspending")
