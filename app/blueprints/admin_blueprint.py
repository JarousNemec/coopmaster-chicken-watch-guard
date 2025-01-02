from flask import Blueprint, make_response

from app.cron.chicken_repoter import check_chicken

admin_blueprint = Blueprint('admin_blueprint', __name__)


@admin_blueprint.route("/api/predict", methods=['GET'])
def predict():
    response = {"state": "recreated"}
    check_chicken()
    return make_response(response)


@admin_blueprint.route("/api/ping", methods=['GET'])
def ping():
    response = {"ping": "pong"}
    return make_response(response)

