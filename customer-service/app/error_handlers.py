
from flask import jsonify
from app.exceptions.exceptions import (
    AccountNotFoundException,
    InsufficientFundsException,
    TransactionNotFoundException
)

def register_error_handlers(app):
    @app.errorhandler(AccountNotFoundException)
    def handle_account_not_found(e):
        return jsonify({'error': 'Account not found'}), 404

    @app.errorhandler(InsufficientFundsException)
    def handle_insufficient_funds(e):
        return jsonify({'error': 'Insufficient funds'}), 400

    @app.errorhandler(TransactionNotFoundException)
    def handle_transaction_not_found(e):
        return jsonify({'error': 'Transaction not found'}), 404
