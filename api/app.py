import json

from flask import Flask, request

from api.methods import query_to_currency_page, invoke_lambda_


def create_app():
    """
    Create the Flask app.
    """
    application = Flask(__name__)

    if application.debug:
        from werkzeug.debug import DebuggedApplication

        application.wsgi_app = DebuggedApplication(application.wsgi_app, True)

    @application.route("/convertCurrency", methods=["POST"])
    def convert_currency():
        data = query_to_currency_page(data=request.json)
        return json.dumps(data)

    @application.route("/saveMeasure", methods=["GET"])
    def save_measures():
        data = invoke_lambda_()
        return json.dumps(data)

    return application


app = create_app()
