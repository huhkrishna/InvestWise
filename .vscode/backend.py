import pymongo
from passlib.hash import pbkdf2_sha256
import random
import string
from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)

# MongoDB connection setup
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["bank_system"]
users_collection = db["users"]

# Function to generate a unique user id
def generate_user_id():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

@app.route('/create-account', methods=['POST'])
def create_account():
    data = request.json
    full_name = data['full_name']
    email = data['email']
    phone_no = data['phone_no']
    min_balance = data['min_balance']

    user_id = generate_user_id()
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    hashed_password = pbkdf2_sha256.hash(password)

    user_data = {
        "user_id": user_id,
        "full_name": full_name,
        "email": email,
        "phone_no": phone_no,
        "password": hashed_password,
        "balance": min_balance,
        "transactions": [],
        "last_withdrawal_date": None,
        "withdrawal_count": 0
    }

    users_collection.insert_one(user_data)
    return jsonify({"user_id": user_id, "password": password})

@app.route('/check-balance', methods=['POST'])
def check_balance():
    data = request.json
    user_id = data['user_id']
    password = data['password']

    user = users_collection.find_one({"user_id": user_id})
    if user and pbkdf2_sha256.verify(password, user['password']):
        return jsonify({"balance": user['balance']})
    else:
        return jsonify({"error": "Incorrect user ID or password."}), 401

@app.route('/withdraw-money', methods=['POST'])
def withdraw_money():
    data = request.json
    user_id = data['user_id']
    password = data['password']
    amount = data['amount']

    user = users_collection.find_one({"user_id": user_id})

    if not user:
        return jsonify({"error": "User not found."}), 404

    if not pbkdf2_sha256.verify(password, user['password']):
        return jsonify({"error": "Incorrect password."}), 401

    current_date = datetime.now().date().isoformat()
    last_withdrawal_date = user.get('last_withdrawal_date')

    if last_withdrawal_date:
        last_withdrawal_date = datetime.strptime(last_withdrawal_date, "%Y-%m-%d").date()

    if last_withdrawal_date and (datetime.now().date() - last_withdrawal_date).days > 30:
        users_collection.update_one(
            {"user_id": user_id},
            {"$set": {"withdrawal_count": 0, "last_withdrawal_date": current_date}}
        )
        user['withdrawal_count'] = 0

    if user['withdrawal_count'] < 5:
        if amount > user['balance']:
            return jsonify({"error": "Insufficient balance."}), 400

        result = users_collection.update_one(
            {"user_id": user_id},
            {
                "$inc": {"balance": -amount, "withdrawal_count": 1},
                "$push": {"transactions": {"type": "withdraw", "amount": amount, "date": current_date}},
                "$set": {"last_withdrawal_date": current_date}
            }
        )

        updated_user = users_collection.find_one({"user_id": user_id})
        return jsonify({"balance": updated_user['balance']})
    else:
        return jsonify({"error": "Maximum withdrawal limit reached for this month."}), 400

@app.route('/transfer-money', methods=['POST'])
def transfer_money():
    data = request.json
    user_id = data['user_id']
    password = data['password']
    amount = data['amount']
    recipient_id = data['recipient_id']

    user = users_collection.find_one({"user_id": user_id})

    if not user:
        return jsonify({"error": "User not found."}), 404

    if not pbkdf2_sha256.verify(password, user['password']):
        return jsonify({"error": "Incorrect password."}), 401

    recipient = users_collection.find_one({"user_id": recipient_id})
    if not recipient:
        return jsonify({"error": "Recipient not found."}), 404

    if user['withdrawal_count'] < 5:
        if amount > user['balance']:
            return jsonify({"error": "Insufficient balance."}), 400

        users_collection.update_one(
            {"user_id": user_id},
            {
                "$inc": {"balance": -amount},
                "$push": {"transactions": {"type": "transfer", "amount": amount, "date": datetime.now().date().isoformat()}},
                "$set": {"last_withdrawal_date": datetime.now().date().isoformat()}
            }
        )

        users_collection.update_one(
            {"user_id": recipient_id},
            {
                "$inc": {"balance": amount},
                "$push": {"transactions": {"type": "credit", "amount": amount, "date": datetime.now().date().isoformat()}}
            }
        )

        updated_user = users_collection.find_one({"user_id": user_id})
        return jsonify({"balance": updated_user['balance']})
    else:
        return jsonify({"error": "Maximum transfer limit reached for this month."}), 400

@app.route('/credit-money', methods=['POST'])
def credit_money():
    data = request.json
    user_id = data['user_id']
    password = data['password']
    amount = data['amount']

    user = users_collection.find_one({"user_id": user_id})

    if not user:
        return jsonify({"error": "User not found."}), 404

    if not pbkdf2_sha256.verify(password, user['password']):
        return jsonify({"error": "Incorrect password."}), 401

    result = users_collection.update_one(
        {"user_id": user_id},
        {
            "$inc": {"balance": amount},
            "$push": {"transactions": {"type": "credit", "amount": amount, "date": datetime.now().date().isoformat()}}
        }
    )

    updated_user = users_collection.find_one({"user_id": user_id})
    return jsonify({"balance": updated_user['balance']})

if __name__ == "__main__":
    app.run(debug=True)
