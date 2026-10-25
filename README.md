# Personal Expense Tracker

This is a small Python program for keeping track of everyday spending from the
terminal. It stores expenses in a CSV file, so the records are still there when
the program is closed and opened again.

## Features

- Add, view, edit and delete expenses
- Keep the date, amount, category and an optional note for each expense
- Show totals by category and by month
- Compare this month's category totals with budget limits
- Display a bar chart of category spending (optional)

## Requirements

- Python 3.8 or newer
- `matplotlib` only if you want to use the chart option

## Run the program

Open a terminal in this folder and run:

```bash
python3 expense_tracker.py
```

On Windows, `python expense_tracker.py` may be the correct command depending
on how Python was installed.

Choose an item from the menu. The program writes changes to `expenses.csv`
after adding, editing or deleting a record. You do not need to save manually.

To use the chart, install matplotlib:

```bash
python -m pip install matplotlib
```

## Data format

The CSV file is created automatically. Its columns are:

```text
id,date,amount,category,note
```

Example:

```text
id,date,amount,category,note
1,2026-10-05,2750.00,Food,weekly groceries
2,2026-10-06,120.00,Travel,bus fare
```

Keep the header as shown above. If the program finds a different header, it
stops rather than overwriting a file it may not understand.

## Example Output

The following is an illustrative example of the program's command-line interface,
not a screenshot of an actual execution.
```text
Personal Expense Tracker
Loaded 2 expense(s) from expenses.csv.

========== Expense Tracker ==========
1. Add an expense
2. Show all expenses
3. Edit an expense
4. Delete an expense
5. View spending summary
6. Check monthly budgets
7. Show category chart
8. Exit

Choose an option: 2

-- Expenses --
  ID  Date             Amount  Category        Note
---------------------------------------------------
   1  2026-10-05    Rs. 250.00  Food            Lunch
   2  2026-10-06    Rs. 120.00  Travel          Bus fare
---------------------------------------------------
2 expense(s) | Total: Rs. 370.00
```

The displayed records and amounts are examples. Actual output depends on the contents of expenses.csv.

## Changing the budgets

The `BUDGETS` dictionary near the top of `expense_tracker.py` sets the monthly
limit for each category. Edit the values to suit your own plan, or add and
remove categories. Category names must match exactly, so `Food` and `food` are
treated as separate categories.

## Current limitations

- Amounts are recorded in rupees; currency conversion is not included.
- Data is kept in one local CSV file. There is no cloud sync or automatic backup.
- Categories are free text, so spelling and capitalization affect the totals.
- Budget checks cover individual categories in the current calendar month.
- The chart opens a window; it does not export an image.
- Deleting an entry cannot be undone, so the program asks for confirmation.
- Invalid rows are skipped with a warning, but the next save removes them from the file.
- Dates are not validated when the file is loaded.

## What I learned
- How to use Python functions to divide a program into smaller, reusable tasks.
- How to store and retrieve expense records using CSV files.
- How to use lists and dictionaries to manage structured data.
- How to validate user input, including dates and expense amounts.
- How to calculate spending totals by category and month.
- How to use exception handling to manage invalid input and file-related errors.
- How to generate a bar chart using Matplotlib.

## Test Cases

-- TEST CASE -> INPUT OR ACTION -> EXPECTED RESULT.
- Add expense -> Enter a valid date, positive amount, category, and note -> Expense is added and saved.
- Invalid amount -> Enter text instead of a number -> Program requests a valid amount.
- Non-positive amount -> Enter zero or a negative amount -> Program rejects it and asks again.
- Invalid date -> Enter an impossible date -> Program requests a valid date.
- View expenses -> Select option 2 when records exist -> Records and overall total are displayed.

## Notes on implementation

The program uses Python's built-in `csv`, `datetime`, `os` and `math` modules.
Input functions check dates and amounts before they are stored, 
and the expense list is split into smaller functions for the menu options.

AI tools were used to assist with debugging guidance and review of the final code.