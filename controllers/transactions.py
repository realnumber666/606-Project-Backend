import json
from models.transactions import get_expenses, add_expense


class TransactionController:
    @staticmethod
    def get_expenses():
        transactions = get_expenses()

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
    def add_expense(record_id, amount, description, datetime, category):
        add_expense(record_id, amount, description, datetime, category)
        return {
            'status': 200,
            'data': {}
        }

