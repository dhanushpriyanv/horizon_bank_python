# app/delegates/customer_delegate.py
from app.services import customer_service

def create_customer(data):
    # You can add pre-processing or validation here if needed
    return customer_service.create_customer(data)

def get_all_customers():
    return customer_service.get_all_customers()
