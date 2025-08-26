from flask import jsonify

from flask import Blueprint, request, jsonify
from app.services.account_service import (
    create_account,
    get_account_by_id,
    get_all_accounts,
    delete_account,
    get_account_by_username,
    get_account_by_customer_id,
    deposit_to_account
)
from app.schemas.account_schema import AccountSchema
from app.exceptions.exceptions import AccountNotFoundException

account_bp = Blueprint("account", __name__, url_prefix="/api/accounts")


@account_bp.route('/create', methods=['POST'])
def create():
    data = request.get_json()
    schema = AccountSchema()
    account_data = schema.load(data)
    account = create_account(account_data)
    return jsonify(schema.dump(account, many=True)), 201


@account_bp.route('/<int:id>', methods=['GET'])
def get_by_id(id):
    account = get_account_by_id(id)
    schema = AccountSchema()
    return jsonify(schema.dump(account, many=True)), 200


@account_bp.route('/', methods=['GET'])
def get_all():
    accounts = get_all_accounts()
    schema = AccountSchema(many=True)
    return jsonify(schema.dump(accounts, many=True)), 200


@account_bp.route('/username', methods=['GET'])
def get_by_username():
    username = request.args.get('username')
    account = get_account_by_username(username)
    schema = AccountSchema()
    return jsonify(schema.dump(account, many=True)), 200


@account_bp.route('/customer/<int:customer_id>', methods=['GET'])
def get_by_customer_id(customer_id):
    account = get_account_by_customer_id(customer_id)
    schema = AccountSchema()
    # return jsonify(schema.dump(account, many=True)), 200
    # return jsonify(schema.dump(account, many=False)), 200
    return jsonify(schema.dump(account)), 200



@account_bp.route('/add-money', methods=['POST'])
def add_money():
    data = request.get_json()
    # customer_id = data.get("customer_id")
    customer_id = data.get("customer_id") or data.get("customerId")
    amount = data.get("amount")
    updated_account = deposit_to_account(customer_id, amount)
    schema = AccountSchema()
    # return jsonify(schema.dump(updated_account, many=True)), 200
    return jsonify(schema.dump(updated_account)), 200

