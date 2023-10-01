import sqlite3

# create SQLite db connection
conn = sqlite3.connect('expenses.db')
cursor = conn.cursor()

conn.commit()


def get_expenses():
    cursor.execute('''
        SELECT TransactionID, Amount, Date, Description, Category
        FROM Transactions
    ''')
    res = cursor.fetchall()

    return res


def add_expense(record_id, amount, description, datetime, category):
    cursor.execute('''
        INSERT INTO Transactions (TransactionID, Amount, Description, Date, Category)
        VALUES (?, ?, ?, ?, ?)
    ''', (record_id, amount, description, datetime, category))
    conn.commit()
