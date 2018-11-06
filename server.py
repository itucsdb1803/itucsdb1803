import os
from flask import Flask
from database import DatabaseOperations

app = Flask(__name__)

@app.route("/")
def home_page():
    db = DatabaseOperations()
    db.create_tables()
    return "Hello World"


if __name__ == '__main__':
    port = app.config.get("PORT", 5000)
    debug = True
    app.run(host='0.0.0.0', port=port, debug=debug)
