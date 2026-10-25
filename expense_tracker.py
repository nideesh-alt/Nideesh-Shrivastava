#!/usr/bin/env python3
"""A small command-line expense tracker that saves records in a CSV file."""

import csv
import math
import os
from datetime import datetime

DATA_FILE = "expenses.csv"
COLUMNS = ["id", "date", "amount", "category", "note"]

BUDGETS = {
    "Food": 3000.00,
    "Travel": 2000.00,
    "Study": 1500.00,
}
BAR_SIZE = 20

MENU = """
========== Expense Tracker ==========
1. Add an expense
2. Show all expenses
3. Edit an expense
4. Delete an expense
5. View spending summary
6. Check monthly budgets
7. Show category chart
8. Exit
"""


def load_expenses():
    """Load saved expenses. A missing or empty file is treated as a new start."""
    if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
        return []

    expenses = []
    with open(DATA_FILE, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        if reader.fieldnames != COLUMNS:
            raise ValueError(
                f"{DATA_FILE} has an unexpected header. "
                f"Expected: {','.join(COLUMNS)}"
            )

        for line_number, row in enumerate(reader, start=2):
            try:
                amount = float(row["amount"])
                expense = {
                    "id": int(row["id"]),
                    "date": row["date"].strip(),
                    "amount": round(amount, 2),
                    "category": row["category"].strip(),
                    "note": (row.get("note") or "").strip(),
                }
                if not math.isfinite(amount) or amount <= 0:
                    raise ValueError
                expenses.append(expense)
            except (TypeError, ValueError, KeyError):
                print(f"Warning: skipped invalid row {line_number} in {DATA_FILE}.")

    return expenses


def save_expenses(expenses):
    """Write to a temporary file first so an interrupted save is less risky."""
    temporary_file = DATA_FILE + ".tmp"
    with open(temporary_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=COLUMNS)
        writer.writeheader()

        for item in sorted(expenses, key=lambda expense: expense["id"]):
            writer.writerow({
                "id": item["id"],
                "date": item["date"],
                "amount": f"{item['amount']:.2f}",
                "category": item["category"],
                "note": item["note"],
            })

    os.replace(temporary_file, DATA_FILE)


def next_expense_id(expenses):
    """Return an ID that has not been used yet."""
    return max((item["id"] for item in expenses), default=0) + 1


def money(amount):
    return f"Rs. {amount:,.2f}"


def expense_text(item):
    text = (
        f"#{item['id']} | {item['date']} | "
        f"{money(item['amount'])} | {item['category']}"
    )
    if item["note"]:
        text += f" | {item['note']}"
    return text


def get_date():
    """Keep asking until the date is a real date written as YYYY-MM-DD."""
    while True:
        value = input("Date (YYYY-MM-DD): ").strip()
        try:
            parsed = datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            print("Enter a valid date, for example 2026-10-24.")
            continue

        # strptime accepts some unpadded dates, so check the original format too.
        if parsed.strftime("%Y-%m-%d") != value:
            print("Use two digits for month and day, e.g. 2026-01-04.")
            continue
        return value


def get_amount():
    while True:
        value = input("Amount in rupees: ").strip()
        try:
            amount = float(value)
        except ValueError:
            print("Enter a number such as 250 or 250.50.")
            continue

        if not math.isfinite(amount) or amount <= 0:
            print("The amount must be greater than zero.")
            continue
        return round(amount, 2)


def get_category():
    while True:
        category = input("Category (Food, Travel, Study, etc.): ").strip()
        if category:
            return category
        print("A category is required.")


def get_note():
    return input("Note (optional): ").strip()


def get_id(prompt):
    try:
        return int(input(prompt).strip())
    except ValueError:
        print("Enter an expense ID using whole numbers.")
        return None


def find_expense(expenses, expense_id):
    for item in expenses:
        if item["id"] == expense_id:
            return item
    return None


def add_expense(expenses):
    print("\n-- Add expense --")
    item = {
        "id": next_expense_id(expenses),
        "date": get_date(),
        "amount": get_amount(),
        "category": get_category(),
        "note": get_note(),
    }
    expenses.append(item)
    save_expenses(expenses)
    print("Saved:", expense_text(item))


def show_expenses(expenses):
    print("\n-- Expenses --")
    if not expenses:
        print("No expenses have been added yet.")
        return

    headings = f"{'ID':>4}  {'Date':10}  {'Amount':>14}  {'Category':<14}  Note"
    print(headings)
    print("-" * len(headings))

    for item in sorted(expenses, key=lambda expense: expense["id"]):
        print(
            f"{item['id']:>4}  {item['date']:10}  "
            f"{money(item['amount']):>14}  "
            f"{item['category']:<14}  {item['note']}"
        )

    total = sum(item["amount"] for item in expenses)
    print("-" * len(headings))
    print(f"{len(expenses)} expense(s) | Total: {money(total)}")


def edit_expense(expenses):
    print("\n-- Edit expense --")
    if not expenses:
        print("There are no expenses to edit.")
        return

    expense_id = get_id("ID to edit: ")
    if expense_id is None:
        return

    item = find_expense(expenses, expense_id)
    if item is None:
        print("That ID was not found.")
        return

    print("Current record:", expense_text(item))
    print("1. Date  2. Amount  3. Category  4. Note  5. Cancel")
    choice = input("Field to change: ").strip()

    if choice == "1":
        item["date"] = get_date()
    elif choice == "2":
        item["amount"] = get_amount()
    elif choice == "3":
        item["category"] = get_category()
    elif choice == "4":
        item["note"] = get_note()
    elif choice == "5":
        print("No changes made.")
        return
    else:
        print("Unknown option. No changes made.")
        return

    save_expenses(expenses)
    print("Updated:", expense_text(item))


def delete_expense(expenses):
    print("\n-- Delete expense --")
    if not expenses:
        print("There are no expenses to delete.")
        return

    expense_id = get_id("ID to delete: ")
    if expense_id is None:
        return

    item = find_expense(expenses, expense_id)
    if item is None:
        print("That ID was not found.")
        return

    answer = input(f"Delete {expense_text(item)}? [y/N]: ").strip().lower()
    if answer not in ("y", "yes"):
        print("Deletion cancelled.")
        return

    expenses.remove(item)
    save_expenses(expenses)
    print("Expense deleted.")


def category_totals(expenses, month=None):
    totals = {}
    for item in expenses:
        if month and not item["date"].startswith(month):
            continue
        category = item["category"]
        totals[category] = totals.get(category, 0.0) + item["amount"]
    return totals


def monthly_totals(expenses):
    totals = {}
    for item in expenses:
        month = item["date"][:7]
        totals[month] = totals.get(month, 0.0) + item["amount"]
    return totals


def show_summary(expenses):
    print("\n-- Spending summary --")
    if not expenses:
        print("Add some expenses first to see a summary.")
        return

    by_category = category_totals(expenses)
    by_month = monthly_totals(expenses)
    this_month = datetime.now().strftime("%Y-%m")
    current_categories = category_totals(expenses, month=this_month)

    print("Total by category:")
    for category, total in sorted(by_category.items()):
        print(f"  {category:<16} {money(total)}")

    print("\nTotal by month:")
    for month, total in sorted(by_month.items()):
        print(f"  {month:<16} {money(total)}")

    total_spent = sum(item["amount"] for item in expenses)
    print(f"\nOverall: {len(expenses)} expense(s), {money(total_spent)}.")

    if current_categories:
        highest = max(current_categories, key=current_categories.get)
        print(f"Highest category this month: {highest} ({money(current_categories[highest])}).")
        print(f"Spent this month: {money(sum(current_categories.values()))}.")
    else:
        print(f"No expenses recorded for {this_month}.")


def check_budgets(expenses):
    print("\n-- Monthly budget check --")
    if not BUDGETS:
        print("No budgets are set. Edit BUDGETS near the top of this file.")
        return

    this_month = datetime.now().strftime("%Y-%m")
    totals = category_totals(expenses, month=this_month)

    for category, limit in BUDGETS.items():
        spent = totals.get(category, 0.0)
        fraction = spent / limit if limit > 0 else 0
        filled = min(int(fraction * BAR_SIZE), BAR_SIZE)
        bar = "#" * filled + "-" * (BAR_SIZE - filled)
        line = f"{category:<12} [{bar}] {money(spent)} / {money(limit)}"

        if spent > limit:
            print(line + f"  OVER by {money(spent - limit)}")
        elif spent == limit:
            print(line + "  LIMIT REACHED")
        else:
            print(line + f"  {fraction * 100:.0f}% used")

    other_categories = sorted(set(totals) - set(BUDGETS))
    if other_categories:
        print("No budget set for: " + ", ".join(other_categories))


def show_chart(expenses):
    """Display a chart if matplotlib is installed."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("Charts require matplotlib. Install it with: pip install matplotlib")
        return

    totals = category_totals(expenses)
    if not totals:
        print("There is no spending data to chart yet.")
        return

    plt.figure(figsize=(8, 5))
    plt.bar(totals.keys(), totals.values())
    plt.title("Expenses by category")
    plt.xlabel("Category")
    plt.ylabel("Amount (Rs.)")
    plt.tight_layout()
    plt.show()


def main():
    try:
        expenses = load_expenses()
    except (OSError, ValueError) as error:
        print(f"Could not load expenses: {error}")
        return

    print("Personal Expense Tracker")
    print(f"Loaded {len(expenses)} expense(s) from {DATA_FILE}.")

    try:
        while True:
            choice = input(MENU + "Choose an option: ").strip().lower()

            if choice == "1":
                add_expense(expenses)
            elif choice == "2":
                show_expenses(expenses)
            elif choice == "3":
                edit_expense(expenses)
            elif choice == "4":
                delete_expense(expenses)
            elif choice == "5":
                show_summary(expenses)
            elif choice == "6":
                check_budgets(expenses)
            elif choice == "7":
                show_chart(expenses)
            elif choice in ("8", "q", "quit", "exit"):
                break
            else:
                print("Choose a number from 1 to 8.")
    except (EOFError, KeyboardInterrupt):
        print("\nInput cancelled.")

    print(f"Finished. {len(expenses)} expense(s) are saved in {DATA_FILE}.")


if __name__ == "__main__":
    main()
