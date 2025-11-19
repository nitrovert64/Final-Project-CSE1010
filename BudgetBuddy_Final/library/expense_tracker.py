class ExpenseTracker:
    def __init__(self):
        self.expenses = {}
    
    def write_to_file(self,expenses_dict):

        with open("expenses.txt", "a") as file:
            for category, amount in expenses_dict.items():
                category_amount = f"{category}: {amount}"
                file.write(category_amount)
            
        
        


        
       
       

    def add_expenses(self):
        while True:
            try:
                entry = input("Enter your expense, here's an example: Milk 10 ")

                parts = entry.split()
                if len(parts) != 2:
                    raise ValueError("Please enter the item and its amount< e.g., Milk 10")
                
                category = parts[0]
                amount = float(parts[1])

                self.expenses[category] = amount 

            except ValueError as e:

                print(f"Invalid input: {e}")
                print("Try again!")
                continue

            another = input("Add another expense? (y/n): ").lower()
            if another != 'y':
                break

        self.write_to_file(self.expenses)
        
    def get_expenses_details(self):
        print(f"\nExpenses Details:")

        if not self.expenses:
            print("No expenses recorded yet")
        else:
            total = 0 

            for category, amount in self.expenses.items():
                print(f"{category}: ${amount:.2f}")

                total += amount 
            print(f"\nTotal Expenses: ${total:.2f}")
            return total

