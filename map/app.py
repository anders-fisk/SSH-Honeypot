from flask import (
    Flask,
    jsonify
)
from database_implementation import DatabaseModel

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    @app.route('/')
    def hello_world():
        return jsonify({
            "status": "success",
            "message": "Hello World!"
        })

    return app  # do not forget to return the app

db = DatabaseModel()
# add data to database
# db.insert_data(ip)
# show all data
# print(db.show_all_data())
APP = create_app()