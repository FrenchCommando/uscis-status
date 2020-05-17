import os
import json

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

with open(os.path.join(basedir, "secrets.json"), "rb") as f:
    data = json.load(f)

postgres_user = data['user']
postgres_password = data['password']
