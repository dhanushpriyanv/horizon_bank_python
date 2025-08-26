# from flask import jsonify

# from flask import Blueprint, request, jsonify
# from app.services.transaction_service import (
#     send_money,
#     get_transaction_by_id,
#     get_all_transactions,
#     get_transactions_by_customer_id,
#     pay_bill_service
# )
# from app.schemas.transaction_schema import TransactionSchema
# from app.schemas.account_schema import AccountSchema
# from app.services.account_service import get_account_by_customer_id,deposit_to_account
# from app.schemas.transaction_schema import TransactionRequestSchema, TransactionSchema, BillPayRequestSchema


# transaction_bp = Blueprint('transaction', __name__, url_prefix='/api/transactions')

# # @transaction_bp.route('', methods=['POST'])
# # def create_transaction():
# #     data = request.get_json()
# #     schema = TransactionSchema()
# #     transaction_data = schema.load(data)
# #     transaction = send_money(transaction_data)
# #     return jsonify(schema.dump(transaction, many=True)), 201

# @transaction_bp.route('', methods=['POST'])
# def create_transaction():
#     data = request.get_json()
#     # schema = TransactionSchema() ❌ wrong one for request
#     schema = TransactionRequestSchema()  # ✅ should be used
#     transaction_data = schema.load(data)
#     transaction = send_money(transaction_data)
#     return jsonify(TransactionSchema().dump(transaction)), 201


# @transaction_bp.route('/<int:id>', methods=['GET'])
# def get_by_id(id):
#     transaction = get_transaction_by_id(id)
#     schema = TransactionSchema()
#     return jsonify(schema.dump(transaction, many=True)), 200

# @transaction_bp.route('/', methods=['GET'])
# def get_all():
#     transactions = get_all_transactions()
#     schema = TransactionSchema(many=True)
#     return jsonify(schema.dump(transactions, many=True)), 200

# @transaction_bp.route('/customer/<int:customer_id>', methods=['GET'])
# def get_transactions_by_customer(customer_id):
#     transactions = get_transactions_by_customer_id(customer_id)
#     return jsonify(TransactionSchema(many=True).dump(transactions)), 200

# # @transaction_bp.route('/bill-pay', methods=['POST'])
# # def pay_bill():
# #     data = request.get_json()
# #     schema = BillPayRequestSchema()
# #     validated_data = schema.load(data)
# #     transaction = pay_bill_service(**validated_data)
# #     # return transaction_schema.dump(transaction), 200
# #     transaction_schema = TransactionSchema()  # ✅ define this
# #     return transaction_schema.dump(transaction),200


# # @transaction_bp.route('/add-money', methods=['POST'])
# # def add_money():
# #     data = request.get_json()
# #     # customer_id = data.get("customer_id")
# #     customer_id = data.get("customer_id") or data.get("customerId")
# #     amount = data.get("amount")
# #     updated_account = deposit_to_account(customer_id, amount)
# #     schema = AccountSchema()
# #     # return jsonify(schema.dump(updated_account, many=True)), 200
# #     return jsonify(schema.dump(updated_account)), 200

# from app.services.transaction_service import (
#     send_money_by_plsql,
#     pay_bill_by_plsql,
#     add_money_by_plsql
# )
# from app.schemas.transaction_schema import TransactionRequestSchema, BillPayRequestSchema
# from app.schemas.transaction_schema import TransactionSchema
# from flask import request, jsonify

# @transaction_bp.route('/send-money', methods=['POST'])
# @transaction_bp.route('/send-money/plsql', methods=['POST'])
# def send_money_plsql():
#     schema = TransactionRequestSchema()
#     data = schema.load(request.get_json())
#     transaction = send_money_by_plsql(data['fromCustomerId'], data['toCustomerId'], data['amount'])
#     return jsonify(TransactionSchema().dump(transaction)), 200

# @transaction_bp.route('/bill-pay', methods=['POST'])
# @transaction_bp.route('/bill-pay/plsql', methods=['POST'])
# def pay_bill_plsql():
#     schema = BillPayRequestSchema()
#     data = schema.load(request.get_json())
#     transaction = pay_bill_by_plsql(data['customerId'], data['billType'], data['accountNumber'], data['amount'])
#     return jsonify(TransactionSchema().dump(transaction)), 200

# @transaction_bp.route('/add-money', methods=['POST'])
# @transaction_bp.route('/add-money/plsql', methods=['POST'])
# def add_money_plsql():
#     data = request.get_json()
#     customer_id = data.get('customerId')
#     amount = data.get('amount')
#     transaction = add_money_by_plsql(customer_id, amount)
#     return jsonify(TransactionSchema().dump(transaction)), 200


from flask import Blueprint, request, jsonify
from app.services.transaction_service import (
    send_money_by_plsql,
    get_transaction_by_id,
    get_all_transactions,
    get_transactions_by_customer_id,
    pay_bill_by_plsql,
    add_money_by_plsql
)
from app.schemas.transaction_schema import (
    TransactionRequestSchema,
    TransactionSchema,
    BillPayRequestSchema
)
from app.schemas.account_schema import AccountSchema
from app.services.account_service import deposit_to_account

transaction_bp = Blueprint('transaction', __name__, url_prefix='/api/transactions')

@transaction_bp.route('', methods=['POST'])
def create_transaction():
    schema = TransactionRequestSchema()
    data = schema.load(request.get_json())
    transaction = send_money_by_plsql(data['fromCustomerId'], data['toCustomerId'], data['amount'])
    return jsonify(TransactionSchema().dump(transaction)), 200

@transaction_bp.route('/<int:id>', methods=['GET'])
def get_by_id(id):
    transaction = get_transaction_by_id(id)
    schema = TransactionSchema()
    return jsonify(schema.dump(transaction)), 200

@transaction_bp.route('/', methods=['GET'])
def get_all():
    transactions = get_all_transactions()
    schema = TransactionSchema(many=True)
    return jsonify(schema.dump(transactions)), 200

@transaction_bp.route('/customer/<int:customer_id>', methods=['GET'])
def get_transactions_by_customer(customer_id):
    transactions = get_transactions_by_customer_id(customer_id)
    return jsonify(TransactionSchema(many=True).dump(transactions)), 200

@transaction_bp.route('/bill-pay', methods=['POST'])
@transaction_bp.route('/bill-pay/plsql', methods=['POST'])
def bill_pay():
    schema = BillPayRequestSchema()
    data = schema.load(request.get_json())
    transaction = pay_bill_by_plsql(data['customerId'], data['billType'], data['accountNumber'], data['amount'])
    return jsonify(TransactionSchema().dump(transaction)), 200

@transaction_bp.route('/add-money', methods=['POST'])
@transaction_bp.route('/add-money/plsql', methods=['POST'])
def add_money():
    data = request.get_json()
    customer_id = data.get('customerId')
    amount = data.get('amount')
    transaction = add_money_by_plsql(customer_id, amount)
    return jsonify(TransactionSchema().dump(transaction)), 200