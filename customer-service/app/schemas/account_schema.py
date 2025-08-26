# app/schemas/account_schema.py
from marshmallow import Schema, fields

class AccountSchema(Schema):
    id = fields.Integer(dump_only=True)
    account_number = fields.String(required=True)
    balance = fields.Float(required=True)
    customer_id = fields.Integer(required=True)

class AddMoneyRequestSchema(Schema):
    customer_id = fields.Integer(required=True)
    amount = fields.Float(required=True)