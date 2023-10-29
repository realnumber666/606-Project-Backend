import json
from models.transactions import *


class TransactionController:
    @staticmethod
    def get_expenses(year=None, month=None):
        transactions = get_expenses(year, month)

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
    def get_monthly_budget(year, month, user_id):
        res = get_monthly_budget(year, month, user_id)

        return {
            'status': 200,
            'data': res
        }

    @staticmethod
    def add_expense(record_id, amount, description, datetime, category):
        add_expense(record_id, amount, description, datetime, category)
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
    def set_monthly_budget(userID, year, month, totalAmount):
        try:
            set_monthly_budgets(userID, year, month, totalAmount)
            return {
                'status': 200,
                'data': {'status': 'success', 'message': 'Budget updated successfully'}
            }
        except Exception as e:
            return {
                'status': 500,
                'data': {'error_msg': str(e)}
            }
