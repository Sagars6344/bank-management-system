import json
import random
import string
from pathlib import Path

class Bank:
    database = "data.json"
    data = []

    # Load data
    if Path(database).exists():
        try:
            with open(database, "r") as f:
                data = json.load(f)
        except:
            data = []
    else:
        data = []

    @staticmethod
    def save():
        with open(Bank.database, "w") as f:
            json.dump(Bank.data, f, indent=4)

    @staticmethod
    def generate_account():
        chars = random.choices(string.ascii_letters, k=5) + \
                random.choices(string.digits, k=3) + \
                random.choices("!@#$%", k=1)
        random.shuffle(chars)
        return "".join(chars)

    @classmethod
    def find_user(cls, acc, pin):
        return next((u for u in cls.data 
                     if u["accountNo"] == acc and str(u["pin"]) == str(pin)), None)

    @classmethod
    def create_account(cls, name, age, email, pin):
        if len(str(pin)) != 4:
            return "PIN must be 4 digits"

        user = {
            "name": name,
            "age": age,
            "Email": email,
            "pin": int(pin),
            "accountNo": cls.generate_account(),
            "balance": 0
        }

        cls.data.append(user)
        cls.save()
        return user

    @classmethod
    def deposit(cls, acc, pin, amount):
        user = cls.find_user(acc, pin)
        if not user:
            return "User not found"

        if amount <= 0 or amount > 50000:
            return "Invalid amount"

        user["balance"] += amount
        cls.save()
        return "Deposit successful"

    @classmethod
    def withdraw(cls, acc, pin, amount):
        user = cls.find_user(acc, pin)
        if not user:
            return "User not found"

        if amount > user["balance"]:
            return "Insufficient balance"

        user["balance"] -= amount
        cls.save()
        return "Withdraw successful"

    @classmethod
    def delete(cls, acc, pin):
        user = cls.find_user(acc, pin)
        if not user:
            return "User not found"

        cls.data.remove(user)
        cls.save()
        return "Account deleted"