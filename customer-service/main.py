
# from app import create_app
# from app.db import db
# from sqlalchemy import text

# app = create_app()



# if __name__ == '__main__':
#     with app.app_context():
#         # Clear existing data
#         # Delete transactions first (child)
#         # db.session.execute(text("DELETE FROM transaction"))
#         # db.session.execute(text("DELETE FROM account"))
#         # db.session.execute(text("DELETE FROM customer"))
#         db.session.execute(text("TRUNCATE TABLE transactions"))
#         db.session.execute(text("TRUNCATE TABLE accounts"))
#         db.session.execute(text("TRUNCATE TABLE customers"))
#         db.session.commit()
#         # Reset sequences (mimics Spring Boot behavior)
#         try:
#             db.session.execute(text("ALTER SEQUENCE CUSTOMER_SEQ RESTART START WITH 1"))
#             db.session.execute(text("ALTER SEQUENCE ACCOUNT_SEQ RESTART START WITH 1"))
#             db.session.execute(text("ALTER SEQUENCE TRANSACTION_SEQ RESTART START WITH 1"))
#             db.session.commit()
#             print("✅ Sequences reset.")
#         except Exception as e:
#             print("⚠️ Sequence reset skipped or failed:", e)

#         # Insert customers
#         customers = [
#             {"name": "John Doe", "email": "john@example.com"},
#             {"name": "Jane Smith", "email": "jane@example.com"},
#             {"name": "Peter Jones", "email": "peter@example.com"},
#             {"name": "Charlie", "email": "charlie@example.com"},
#         ]

#         for c in customers:
#             db.session.execute(text("""
#                 INSERT INTO customers (id, name, email)
#                 VALUES (CUSTOMER_SEQ.NEXTVAL, :name, :email)
#             """), {"name": c["name"], "email": c["email"]})

#         db.session.commit()

#         # Fetch customer IDs
#         result = db.session.execute(text("SELECT id FROM customers ORDER BY id"))
#         customer_ids = [row[0] for row in result]

#         # Insert accounts
#         for idx, cid in enumerate(customer_ids):
#             db.session.execute(text("""
#                 INSERT INTO accounts (id, account_number, balance, customer_id)
#                 VALUES (ACCOUNT_SEQ.NEXTVAL, :acc_num, :balance, :cid)
#             """), {
#                 "acc_num": f"100{idx+1}",
#                 "balance": 100000.00,
#                 "cid": cid
#             })

#         db.session.commit()
#         print("✅ Seeded customers and accounts using sequences.")

#     # Start Flask server
#     app.run(debug=True, port=8083)


from app import create_app
from app.db import db
from sqlalchemy import text

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # Truncate tables
        db.session.execute(text("TRUNCATE TABLE transactions"))
        db.session.execute(text("TRUNCATE TABLE accounts"))
        db.session.execute(text("TRUNCATE TABLE customers"))
        db.session.commit()

        # Reset sequences
        try:
            db.session.execute(text("ALTER SEQUENCE CUSTOMER_SEQ RESTART START WITH 1"))
            db.session.execute(text("ALTER SEQUENCE ACCOUNT_SEQ RESTART START WITH 1"))
            db.session.execute(text("ALTER SEQUENCE TRANSACTION_SEQ RESTART START WITH 1"))
            db.session.commit()
            print("✅ Sequences reset.")
        except Exception as e:
            print("⚠️ Sequence reset skipped or failed:", e)

        # Insert customers (no email field now)
        customers = [
            {"name": "John Doe"},
            {"name": "Jane Smith"},
            {"name": "Peter Jones"},
            {"name": "Charlie"},
        ]

        for c in customers:
            db.session.execute(text("""
                INSERT INTO customers (id, customer_name)
                VALUES (CUSTOMER_SEQ.NEXTVAL, :name)
            """), {"name": c["name"]})

        db.session.commit()

        # Fetch customer IDs
        result = db.session.execute(text("SELECT id FROM customers ORDER BY id"))
        customer_ids = [row[0] for row in result]

        # Insert accounts
        for idx, cid in enumerate(customer_ids):
            db.session.execute(text("""
                INSERT INTO accounts (id, account_number, balance, customer_id)
                VALUES (ACCOUNT_SEQ.NEXTVAL, :acc_num, :balance, :cid)
            """), {
                "acc_num": f"100{idx+1}",
                "balance": 100000.00,
                "cid": cid
            })

        db.session.commit()
        print("✅ Seeded customers and accounts using sequences.")

    # Start Flask server
    app.run(debug=True, port=8083)
