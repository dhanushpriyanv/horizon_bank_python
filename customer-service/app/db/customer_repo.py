# app/db/customer_repo.py
from app.models.customer import Customer
from app.db import db

def get_all_customers():
    return Customer.query.all()

def get_customer_by_id(customer_id):
    return Customer.query.filter_by(id=customer_id).first()

def create_customer(customer):
    db.session.add(customer)
    db.session.commit()
    return customer

def delete_customer(customer):
    db.session.delete(customer)
    db.session.commit()
