import sqlite3

# create SQLite db connection
conn = sqlite3.connect('expenses.db')
cursor = conn.cursor()

conn.commit()


def get_expenses(year=None, month=None, user=None):
    if year and month and user:
        # Fetch expenses for the given year and month
        cursor.execute('''
            SELECT TransactionID, Amount, Date, Description, Category
            FROM Transactions
            JOIN Users
            ON Transactions.UserID = Users.UserID
            WHERE strftime('%Y', Date) = ? AND strftime('%m', Date) = ? AND Username = ?
            ORDER BY Date DESC
        ''', (year, month, user))
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


def add_expense(record_id, amount, description, datetime, category, username):
    cursor.execute('''
                SELECT UserID
                FROM Users
                WHERE Username = ?
            ''', (username,))
    res = cursor.fetchall()
    user_id = res[0][0]

    cursor.execute('''
        INSERT INTO Transactions (TransactionID, Amount, Description, Date, Category, UserID)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (record_id, amount, description, datetime, category, user_id))
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


def set_monthly_budgets(username, year, month, totalAmount):
    # Check if budget for this user and month already exists
    cursor.execute('''
                    SELECT BudgetID FROM MonthlyBudget
                    JOIN Users
                    ON MonthlyBudget.UserID = Users.UserID
                    WHERE Username = ? AND Year = ? AND Month = ?
                ''', (username, year, month))
    existing_budget = cursor.fetchone()

    user_id_subquery = '(SELECT UserID FROM Users WHERE Username = ?)'
    if existing_budget:
        # Update the existing budget
        cursor.execute(f'''
                                UPDATE MonthlyBudget
                                SET TotalAmount = ?
                                WHERE UserID = {user_id_subquery} AND Year = ? AND Month = ?
                            ''', (totalAmount, username, year, month))
    else:
        # Insert a new budget
        cursor.execute(f'''
                        INSERT INTO MonthlyBudget (UserID, Year, Month, TotalAmount)
                        VALUES ({user_id_subquery}, ?, ?, ?)
                    ''', (username, year, month, totalAmount))
    conn.commit()


def get_monthly_budget(year, month, username=None):
    cursor.execute('''
                SELECT TotalAmount
                FROM MonthlyBudget
                JOIN Users
                ON MonthlyBudget.UserID = Users.UserID
                WHERE Year = ? AND Month = ? AND Username = ?
            ''', (year, month, username))

    res = cursor.fetchall()
    if len(res) == 1:
        return res[0][0]
    else:
        return 0
