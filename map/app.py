from flask import (
    Flask,
    jsonify
)

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


APP = create_app()