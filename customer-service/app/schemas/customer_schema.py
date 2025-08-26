# # app/schemas/customer_schema.py
# from marshmallow import Schema, fields

# class CustomerSchema(Schema):
#     id = fields.Integer(dump_only=True)
#     name = fields.String(required=True)
#     email = fields.String(required=True)


# app/schemas/customer_schema.py
from marshmallow import Schema, fields

class CustomerSchema(Schema):
    id = fields.Int(dump_only=True)
    customerName = fields.String(attribute="customer_name", required=True)
    #email = fields.String(required=True)
