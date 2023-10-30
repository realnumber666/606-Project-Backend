import json
from models.transactions import *


class TransactionController:

    @staticmethod
    def signup(username, password, fullName):
        try:
            # Check if the username already exists in the database
            cursor.execute('SELECT userId FROM Users WHERE username = ?', (username,))
            existing_user = cursor.fetchone()
            if existing_user:
                return {
                    'status': 202,
                    'data': {'error_msg': 'Username already exists'}
                }

            # Get the biggest userId in the database and increment by 1
            cursor.execute('SELECT MAX(userId) FROM Users')
            max_user_id = cursor.fetchone()[0]
            if max_user_id is None:
                max_user_id = 1
            else:
                max_user_id += 1

            # Insert the new user into the Users table
            try:
                cursor.execute('INSERT INTO Users (UserId, username, password, FullName) VALUES (?, ?, ?, ?)',
                            (max_user_id, username, password, fullName))
                conn.commit()
            except Exception as e:
                # Log the exception or print it for debugging
                print(f"Error inserting user: {str(e)}")
                conn.rollback()


            return {
                'status': 200,
                'data': {}
            }
        except Exception as e:
            return {
                'status': 500,
                'data': {'error_msg': str(e)}
            }

    @staticmethod
    def get_expenses(year=None, month=None, user=None):
        transactions = get_expenses(year, month, user)

        # calculate the total amount
        total = sum(transaction[1] for transaction in transactions)

        # build response data
        response_data = {
            'total': total,
            'transactions': [{'record_id': row[0], 'amount': row[1], 'datetime': row[2],
                              'description': row[3], 'category': row[4]} for row in transactions]
        }

        return response_data

    @staticmethod
    def get_monthly_budget(year, month, username):
        res = get_monthly_budget(year, month, username)

        return {
            'status': 200,
            'data': res
        }

    @staticmethod
    def add_expense(record_id, amount, description, datetime, category, username):
        add_expense(record_id, amount, description, datetime, category, username)
        return {
            'status': 200,
            'data': {}
        }

    @staticmethod
    def delete_expense(record_id):
        delete_expense(record_id)
        return {
            'status': 200,
            'data': {}
        }

    @staticmethod
    def update_expense(record_id, amount, description, datetime, category):
        try:
            update_expense(record_id, amount, description, datetime, category)
            return {
                'status': 200,
                'data': {}
            }
        except Exception as e:
            return {
                'status': 500,
                'data': {'error_msg': str(e)}
            }

    @staticmethod
    def set_monthly_budget(username, year, month, totalAmount):
        try:
            set_monthly_budgets(username, year, month, totalAmount)
            return {
                'status': 200,
                'data': {'status': 'success', 'message': 'Budget updated successfully'}
            }
        except Exception as e:
            return {
                'status': 500,
                'data': {'error_msg': str(e)}
            }
        
    @staticmethod
    def login(username, password):
        try:
            cursor.execute('SELECT * FROM Users WHERE Username = ? AND Password = ?', (username, password))
            user = cursor.fetchone()
            if user:
                return {
                    'status': 200,
                    'data': {}
                }
            else:
                return {
                    'status': 202,
                    'data': {'error_msg': 'Invalid username or password'}
                }
        except Exception as e:
            return {
                'status': 500,
                'data': {'error_msg': str(e)}
            }

