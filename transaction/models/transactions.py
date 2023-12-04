from pymongo import MongoClient
from datetime import datetime as dt
from bson.objectid import ObjectId

# Define the format matching the string format
format_str = "%Y-%m-%dT%H:%M"

# Connect to the MongoDB database server
client = MongoClient("mongodb+srv://ray:luckyray@cluster0.mrq1axf.mongodb.net/?retryWrites=true&w=majority")

# Connect to the database
db = client['expenses_db']

# Get the collections
transactions_collection = db['transactions']
monthly_budget_collection = db['monthly_budget']
days_of_month = {
    1: 31,  # January
    2: 28,  # February (non-leap year)
    3: 31,  # March
    4: 30,  # April
    5: 31,  # May
    6: 30,  # June
    7: 31,  # July
    8: 31,  # August
    9: 30,  # September
    10: 31, # October
    11: 30, # November
    12: 31  # December
}



def get_expenses(year, month, user, category=None):
    # Fetch expenses for the given year and month
    start_date = dt(year, month, 1)
    end_date = dt(year, month, days_of_month[month])
    print(f"get_expenses from {start_date} to {end_date} for {user} {category}")
    if category:
        cursor = transactions_collection.find({
            "username": user,
            "category": category,
            "date": {
                "$gte": start_date,
                "$lte": end_date
            }
        }).sort("date", -1)
    else:
        cursor = transactions_collection.find({
            "username": user,
            "date": {
                "$gte": start_date,
                "$lt": end_date
            }
        }).sort("date", -1)

    return list(cursor)


def add_expense(amount, description, datetime, category, username):
    datetime = dt.strptime(datetime, format_str)
    transaction = {
        "amount": int(amount),
        "description": description,
        "date": datetime,
        "category": category,
        "username": username
    }
    transactions_collection.insert_one(transaction)


def delete_expense(record_id):
    # Assuming record_id is the string representation of MongoDB's ObjectId
    transactions_collection.delete_one({"_id": ObjectId(record_id)})


def update_expense(record_id, amount, description, datetime, category):
    datetime = dt.strptime(datetime, format_str)
    # Assuming record_id is the string representation of MongoDB's ObjectId
    transactions_collection.update_one(
        {"_id": ObjectId(record_id)},
        {"$set": {
            "amount": amount,
            "description": description,
            "date": datetime,
            "category": category
        }}
    )


def set_monthly_budgets(username, year, month, totalAmount):
    # Check if budget for this user and month already exists
    budget_document = monthly_budget_collection.find_one({
        "username": username,
        "year": year,
        "month": month
    })

    if budget_document:
        # Update the existing budget
        monthly_budget_collection.update_one(
            {
                "username": username,
                "year": year,
                "month": month
            },
            {"$set": {"totalAmount": totalAmount}}
        )
    else:
        # Insert a new budget
        monthly_budget_collection.insert_one({
            "username": username,
            "year": year,
            "month": month,
            "totalAmount": totalAmount
        })


def get_monthly_budget(year, month, username):
    budget_document = monthly_budget_collection.find_one({
        "username": username,
        "year": year,
        "month": month
    })
    if budget_document:
        return budget_document["totalAmount"]
    else:
        return 0
