from tests.runtime_agent import init_runtime_logger

from app.db_init import initialize_oracle_objects
# from flask import Flask, jsonify
# from flask_cors import CORS
# from app.db import db
# from app.exceptions.errors import CustomerNotFoundException, AccountNotFoundException, InsufficientFundsException
# from app.controllers.customer_controller import customer_bp
# from app.controllers.account_controller import account_bp
# from app.controllers.transaction_controller import transaction_bp

# def create_app():
        # initialize_oracle_objects()
#     app = Flask(__name__)
    
#     # Load config
#     app.config.from_object('app.config.settings.Config')
#     db.init_app(app)
#     # CORS for React frontend (adjust if needed)
#     CORS(app, resources={r"/*": {"origins": "*"}})

#     # Register blueprints here later
#     # from app.controllers.user_controller import user_bp
#     # app.register_blueprint(user_bp)
#     # Register blueprints (example)

#     app.register_blueprint(customer_bp)
#     app.register_blueprint(account_bp)
#     app.register_blueprint(transaction_bp)

#     # Global exception handling
#     @app.errorhandler(CustomerNotFoundException)
#     def handle_customer_not_found(e):
#         return jsonify({'error': 'Customer not found'}), 404

#     @app.errorhandler(AccountNotFoundException)
#     def handle_account_not_found(e):
#         return jsonify({'error': 'Account not found'}), 404

#     @app.errorhandler(InsufficientFundsException)
#     def handle_insufficient_funds(e):
#         return jsonify({'error': 'Insufficient funds'}), 400

#     @app.errorhandler(Exception)
#     def handle_generic_exception(e):
#         return jsonify({'error': str(e)}), 500
    
#         init_runtime_logger(app)
    # return app


from flask import Flask
from flask_cors import CORS
from app.db import db
from app.config.settings import Config
# import tests.runtime_agent
from tests.runtime_agent import init_runtime_logger
# from tests.runtime_agent import start_runtime_tracing

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    init_runtime_logger(app)
    # start_runtime_tracing()
    # CORS setup
    CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)

    db.init_app(app)

    # ✅ Now wrap this inside app context
    with app.app_context():
        from app.db_init import initialize_oracle_objects
        initialize_oracle_objects()

    # Register controllers
    from app.controllers.customer_controller import customer_bp
    from app.controllers.account_controller import account_bp
    from app.controllers.transaction_controller import transaction_bp

    app.register_blueprint(customer_bp)
    app.register_blueprint(account_bp)
    app.register_blueprint(transaction_bp, url_prefix='/api/transactions')

    @app.route('/api/health/db')
    def db_health_check():
        try:
            from sqlalchemy import text
            result = db.session.execute(text("SELECT 'Oracle OK' AS status FROM dual"))
            return {"status": result.fetchone()[0]}
        except Exception as e:
            return {"status": "error", "details": str(e)}, 500

        # init_runtime_logger(app)
    return app

