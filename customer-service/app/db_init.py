
from app.db import db
from sqlalchemy import text

def initialize_oracle_objects():
    # Table and sequence creation statements (idempotent via exception handling)
    ddl_statements = [
        # CUSTOMER TABLE
        """
        BEGIN
            EXECUTE IMMEDIATE 'CREATE TABLE customers (
                id NUMBER PRIMARY KEY,
                customer_name VARCHAR2(100) NOT NULL
                
            )';
        EXCEPTION
            WHEN OTHERS THEN
                IF SQLCODE != -955 THEN
                    RAISE;
                END IF;
        END;
        """,

        # CUSTOMER SEQUENCE
        """
        BEGIN
            EXECUTE IMMEDIATE 'CREATE SEQUENCE customer_seq START WITH 1 INCREMENT BY 1';
        EXCEPTION
            WHEN OTHERS THEN
                IF SQLCODE != -955 THEN
                    RAISE;
                END IF;
        END;
        """,

        # ACCOUNT TABLE
        """
        BEGIN
            EXECUTE IMMEDIATE 'CREATE TABLE accounts (
                id NUMBER PRIMARY KEY,
                account_number VARCHAR2(20) NOT NULL,
                customer_id NUMBER NOT NULL,
                balance FLOAT NOT NULL
            )';
        EXCEPTION
            WHEN OTHERS THEN
                IF SQLCODE != -955 THEN
                    RAISE;
                END IF;
        END;
        """,

        # ACCOUNT SEQUENCE
        """
        BEGIN
            EXECUTE IMMEDIATE 'CREATE SEQUENCE account_seq START WITH 1 INCREMENT BY 1';
        EXCEPTION
            WHEN OTHERS THEN
                IF SQLCODE != -955 THEN
                    RAISE;
                END IF;
        END;
        """,

        # TRANSACTION TABLE
        """
        BEGIN
            EXECUTE IMMEDIATE 'CREATE TABLE transactions (
                id NUMBER PRIMARY KEY,
                amount FLOAT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                type VARCHAR2(20),
                account_id NUMBER NOT NULL,
                from_customer NUMBER,
                to_customer NUMBER
            )';
        EXCEPTION
            WHEN OTHERS THEN
                IF SQLCODE != -955 THEN
                    RAISE;
                END IF;
        END;
        """,

        # TRANSACTION SEQUENCE
        """
        BEGIN
            EXECUTE IMMEDIATE 'CREATE SEQUENCE transaction_seq START WITH 1 INCREMENT BY 1';
        EXCEPTION
            WHEN OTHERS THEN
                IF SQLCODE != -955 THEN
                    RAISE;
                END IF;
        END;
        """
    ]

    for ddl in ddl_statements:
        db.session.execute(text(ddl))
    db.session.commit()
