
from functools import wraps
from app.db import db
from sqlalchemy.exc import SQLAlchemyError

def transactional(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            db.session.commit()
            return result
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    return wrapper
