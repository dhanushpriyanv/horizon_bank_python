from flask import jsonify

from flask import Blueprint, request, jsonify
from app.services.customer_service import (
    create_customer,
    get_customer_by_id,
    get_all_customers,
    update_customer,
    delete_customer
)
from app.schemas.customer_schema import CustomerSchema
from app.exceptions.exceptions import CustomerNotFoundException

customer_bp = Blueprint('customer', __name__, url_prefix='/api/customers')


@customer_bp.route('', methods=['POST'])
def create():
    data = request.get_json()
    schema = CustomerSchema()
    customer_data = schema.load(data)
    customer = create_customer(customer_data)
    return jsonify(schema.dump(customer, many=True)), 201


@customer_bp.route('/', methods=['GET'])
def get_all():
    customers = get_all_customers()
    schema = CustomerSchema(many=True)
    return jsonify(schema.dump(customers, many=True)), 200


@customer_bp.route('/<int:id>', methods=['GET'])
def get_by_id(id):
    customer = get_customer_by_id(id)
    if not customer:
        raise CustomerNotFoundException(f"Customer {id} not found")
    schema = CustomerSchema()
    return jsonify(schema.dump(customer, many=True)), 200


@customer_bp.route('/<int:id>', methods=['PUT'])
def update(id):
    data = request.get_json()
    schema = CustomerSchema()
    customer_data = schema.load(data)
    updated_customer = update_customer(id, customer_data)
    return jsonify(schema.dump(updated_customer, many=True)), 200


@customer_bp.route('/<int:id>', methods=['DELETE'])
def delete(id):
    delete_customer(id)
    return jsonify({'message': 'Customer deleted successfully'}), 200
