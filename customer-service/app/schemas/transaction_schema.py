# # app/schemas/transaction_schema.py
from marshmallow import Schema, fields
from app.schemas.customer_schema import CustomerSchema
from datetime import datetime

from marshmallow import Schema, fields


#### working python
# class TransactionSchema(Schema):
#     id = fields.Int(dump_only=True)
#     amount = fields.Float(required=True)
#     sender_account_id = fields.Int()
#     receiver_account_id = fields.Int()
#     timestamp = fields.DateTime()
#     fromCustomer = fields.Nested(CustomerSchema, dump_only=True)
#     toCustomer = fields.Nested(CustomerSchema, dump_only=True)

    
class TransactionRequestSchema(Schema):
    fromCustomerId = fields.Int(required=True)
    toCustomerId = fields.Int(required=True)
    amount = fields.Float(required=True)



class TransactionSchema(Schema):
    id = fields.Int(dump_only=True)
    amount = fields.Float(required=True)
    timestamp = fields.DateTime(dump_only=True)
    type = fields.Str(required=True)

    account_id = fields.Int(required=True)
    from_customer = fields.Int(allow_none=True)
    to_customer = fields.Int(allow_none=True)

    # Optionally include full customer info for display
    fromCustomer = fields.Nested(CustomerSchema, attribute="from_customer_ref", dump_only=True)
    toCustomer = fields.Nested(CustomerSchema, attribute="to_customer_ref", dump_only=True)


class BillPayRequestSchema(Schema):
    customerId = fields.Int(required=True)
    billType = fields.Str(required=True)
    accountNumber = fields.Str(required=True)
    amount = fields.Float(required=True)
