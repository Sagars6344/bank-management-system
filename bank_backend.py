import json
import random
import string
from pathlib import Path
from datetime import datetime

class Bank:
    database = "data.json"
    data = []

    # ----------- LOAD DATA -----------
    if Path(database).exists():
        try:
            with open(database, "r") as f:
                data = json.load(f)
        except:
            data = []
    else:
        data = []

    # ----------- SAVE DATA -----------
    @staticmethod
    def save():
        with open(Bank.database, "w") as f:
            json.dump(Bank.data, f, indent=4)

    # ----------- ACCOUNT GENERATOR -----------
    @staticmethod
    def generate_account():
        while True:
            chars = random.choices(string.ascii_letters, k=5) + \
                    random.choices(string.digits, k=3) + \
                    random.choices("!@#$%", k=1)
            random.shuffle(chars)
            acc = "".join(chars)

            # ensure unique account number
            if not any(u["accountNo"] == acc for u in Bank.data):
                return acc

    # ----------- FIND USER -----------
    @classmethod
    def find_user(cls, acc, pin):
        return next((u for u in cls.data 
                     if u["accountNo"] == acc and str(u["pin"]) == str(pin)), None)

    @classmethod
    def find_by_email(cls, email, pin):
        return next((u for u in cls.data 
                     if u["Email"] == email and str(u["pin"]) == str(pin)), None)

    # ----------- CREATE ACCOUNT -----------
    @classmethod
    def create_account(cls, name, age, email, pin):

        if not name or not email:
            return "All fields are required"

        if len(str(pin)) != 4:
            return "PIN must be 4 digits"

        # 🔥 prevent duplicate email
        if any(u["Email"] == email for u in cls.data):
            return "Email already registered"

        user = {
            "name": name,
            "age": age,
            "Email": email,
            "pin": int(pin),
            "accountNo": cls.generate_account(),
            "balance": 0,
            "transactions": []
        }

        cls.data.append(user)
        cls.save()
        return user

    # ----------- DEPOSIT -----------
    @classmethod
    def deposit(cls, acc, pin, amount):
        user = cls.find_user(acc, pin)
        if not user:
            return "User not found"

        if amount <= 0 or amount > 50000:
            return "Invalid amount"

        # 🔥 safety for old users
        if "transactions" not in user:
            user["transactions"] = []

        user["balance"] += amount

        user["transactions"].append({
            "type": "Deposit",
            "amount": amount,
            "time": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        })

        cls.save()
        return "Deposit successful"

    # ----------- WITHDRAW -----------
    @classmethod
    def withdraw(cls, acc, pin, amount):
        user = cls.find_user(acc, pin)
        if not user:
            return "User not found"

        if amount <= 0:
            return "Invalid amount"

        if amount > user["balance"]:
            return "Insufficient balance"

        # 🔥 safety
        if "transactions" not in user:
            user["transactions"] = []

        user["balance"] -= amount

        user["transactions"].append({
            "type": "Withdraw",
            "amount": amount,
            "time": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        })

        cls.save()
        return "Withdraw successful"

    # ----------- PASSBOOK -----------
    @classmethod
    def get_passbook(cls, email, pin):
        user = cls.find_by_email(email, pin)

        if not user:
            return None

        # 🔥 safety fix
        if "transactions" not in user:
            user["transactions"] = []

        return {
            "name": user["name"],
            "accountNo": user["accountNo"],
            "balance": user["balance"],
            "transactions": user["transactions"]
        }

    # ----------- DELETE -----------
    @classmethod
    def delete(cls, acc, pin):
        user = cls.find_user(acc, pin)
        if not user:
            return "User not found"

        cls.data.remove(user)
        cls.save()
        return "Account deleted"