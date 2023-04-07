import os

HOST = os.environ.get('HOST', 'mongo_extension_mongo')
PORT = os.environ.get('PORT')
USERNAME = os.environ.get('USERNAME')
PASSWORD = os.environ.get('PASSWORD')
DB = os.environ.get('DB')
if PORT:
    PORT = int(PORT)