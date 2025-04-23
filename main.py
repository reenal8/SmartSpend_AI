import csv
from datetime import datetime
from collections import defaultdict
from sklearn.linear_model import LinearRegression
import numpy as np

# 🔹 Add a new expense
def add_expense(amount, category, note):
    date = datetime.now().strftime("%Y-%m-%d")
    with open('expenses.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, amount, category, note])
    print("💸 Expense added!")

# 🔹 View all expenses
def view_expenses():
    with open('expenses.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            print(row)

# 🔹 Summarize expenses by category
def summarize_expenses():
    categories = defaultdict(float)  # Using defaultdict to sum expenses by category
    with open('expenses.csv', 'r') as file:
        reader = csv.reader(file)
        header = next(reader)  # Skip the header row

        # Ensure that we're processing only valid rows (i.e., rows with data)
        for row in reader:
            if row and len(row) > 1 and row[1].replace('.', '', 1).isdigit():  # Skip empty rows and ensure the amount is a number
                try:
                    category = row[2]
                    amount = float(row[1])  # Convert amount to float
                    categories[category] += amount
                except ValueError:
                    print(f"Skipping invalid row: {row}")  # Handle any invalid rows gracefully
            else:
                print(f"Skipping invalid or empty row: {row}")
                
    print("\n💰 Expenses by Category:")
    if categories:
        for category, total in categories.items():
            print(f"{category}: ₹{total:.2f}")
    else:
        print("No valid expenses to summarize.")
    
    return categories

    print("\n💰 Expenses by Category:")
    for category, total in categories.items():
        print(f"{category}: ₹{total:.2f}")
    
    return categories

# 🔹 Predict budget using simple regression model
def predict_budget(categories):
    # Data preparation: features and target
    features = np.array([[total] for total in categories.values()])  # Each category's total as feature
    target = np.array([sum(categories.values())])  # Single target: the total expenditure

    # Check if we have enough data to proceed
    if len(features) < 2:  # Need at least 2 data points to train a model
        print("Not enough data to predict budget. Please add more expenses.")
        return

    # Train the regression model
    model = LinearRegression()
    model.fit(features, np.repeat(target, len(features)))  # Repeat target to match the number of features

    # Predict monthly budget (we’ll predict based on the past expenses)
    predicted_budget = model.predict(features)
    print(f"\n💡 Suggested Monthly Budget: ₹{predicted_budget[0]:.2f}")

# 🔹 Main Menu
def main():
    while True:
        print("\n📋 What do you want to do?")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. View Expenses by Category")
        print("4. Get AI Budget Suggestion")
        print("5. Exit")

        choice = input("👉 Enter your choice: ")

        if choice == '1':
            amt = input("Enter amount: ₹")
            cat = input("Enter category (food, travel, etc.): ")
            note = input("Add a note (optional): ")
            add_expense(amt, cat, note)
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            summarize_expenses()
        elif choice == '4':
            categories = summarize_expenses()  # Get the category-wise summary
            predict_budget(categories)  # Predict the budget
        elif choice == '5':
            print("Bye bestie 💖")
            break
        else:
            print("Invalid choice! Try again.")

if __name__ == "__main__":
    main()
