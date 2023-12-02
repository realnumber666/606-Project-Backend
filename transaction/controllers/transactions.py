import json
from models.transactions import *
import datetime as dt


format_str = "%Y-%m-%d %H:%M"


class TransactionController:
    @staticmethod
    def get_expenses(year, month, user):
        transactions = get_expenses(int(year), int(month), user)
        print(transactions)

        # calculate the total amount
        total = sum(transaction['amount'] for transaction in transactions)

        # build response data
        response_data = {
            'total': total,
            'transactions': [{'record_id': str(row['_id']), 'amount': row['amount'], 'datetime': row['date'].strftime(format_str),
                              'description': row['description'], 'category': row['category']} for row in transactions]
        }

        return response_data

    @staticmethod
    def get_monthly_budget(year, month, username):
        res = get_monthly_budget(int(year), int(month), username)

        return {
            'status': 200,
            'data': res
        }

    @staticmethod
    def add_expense(amount, description, datetime, category, username):
        add_expense(amount, description, datetime, category, username)
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
