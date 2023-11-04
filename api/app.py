from flask import Flask, jsonify, request

from api.methods import query_to_currency_page


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
        return jsonify(message=data)

    return application


app = create_app()
