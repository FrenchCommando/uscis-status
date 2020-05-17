import json


with open("secrets.json", "rb") as f:
    data = json.load(f)

postgres_user = data['user']
postgres_password = data['password']
