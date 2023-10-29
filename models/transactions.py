import sqlite3

# create SQLite db connection
conn = sqlite3.connect('expenses.db')
cursor = conn.cursor()

conn.commit()


def get_expenses(year=None, month=None):
    if year and month:
        # Fetch expenses for the given year and month
        cursor.execute('''
            SELECT TransactionID, Amount, Date, Description, Category
            FROM Transactions
            WHERE strftime('%Y', Date) = ? AND strftime('%m', Date) = ?
            ORDER BY Date DESC
        ''', (year, month))
    else:
        # Fetch the latest 30 expenses
        cursor.execute('''
            SELECT TransactionID, Amount, Date, Description, Category
            FROM Transactions
            ORDER BY Date DESC
            LIMIT 30
        ''')

    res = cursor.fetchall()
    return res


def add_expense(record_id, amount, description, datetime, category):
    cursor.execute('''
        INSERT INTO Transactions (TransactionID, Amount, Description, Date, Category)
        VALUES (?, ?, ?, ?, ?)
    ''', (record_id, amount, description, datetime, category))
    conn.commit()


def delete_expense(record_id):
    cursor.execute('''
        DELETE FROM Transactions
        WHERE TransactionID = ?
    ''', (record_id,))
    conn.commit()


def update_expense(record_id, amount, description, datetime, category):
    cursor.execute('''
        UPDATE Transactions
        SET Amount = ?, Description = ?, Date = ?, Category = ?
        WHERE TransactionID = ?
    ''', (amount, description, datetime, category, record_id))
    conn.commit()


def set_monthly_budgets(userID, year, month, totalAmount):
    # Check if budget for this user and month already exists
    cursor.execute('''
                    SELECT BudgetID FROM MonthlyBudget
                    WHERE UserID = ? AND Year = ? AND Month = ?
                ''', (userID, year, month))
    existing_budget = cursor.fetchone()

    if existing_budget:
        # Update the existing budget
        cursor.execute('''
                        UPDATE MonthlyBudget
                        SET TotalAmount = ?
                        WHERE UserID = ? AND Year = ? AND Month = ?
                    ''', (totalAmount, userID, year, month))
    else:
        # Insert a new budget
        cursor.execute('''
                        INSERT INTO MonthlyBudget (UserID, Year, Month, TotalAmount)
                        VALUES (?, ?, ?, ?)
                    ''', (userID, year, month, totalAmount))

    conn.commit()


def get_monthly_budget(year, month, user_id=None):
    cursor.execute('''
                SELECT TotalAmount
                FROM MonthlyBudget
                WHERE Year = ? AND Month = ? AND UserID = ?
            ''', (year, month, user_id))

    res = cursor.fetchall()
    if len(res) == 1:
        return res[0][0]
    else:
        return 0
