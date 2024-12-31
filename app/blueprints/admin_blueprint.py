from flask import Blueprint, make_response

from app.cron.dog_repoter import check_dog

admin_blueprint = Blueprint('admin_blueprint', __name__)


@admin_blueprint.route("/api/predict", methods=['GET'])
def predict():
    response = {"state": "recreated"}
    check_dog()
    return make_response(response)


@admin_blueprint.route("/api/ping", methods=['GET'])
def ping():
    response = {"ping": "pong"}
    return make_response(response)

