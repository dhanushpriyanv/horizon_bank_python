# app/config/settings.py

from app.config import oracle_config

class Config:
    SQLALCHEMY_DATABASE_URI = (
        f"oracle+cx_oracle://{oracle_config.ORACLE_USER}:{oracle_config.ORACLE_PASS}"
        f"@{oracle_config.ORACLE_HOST}:{oracle_config.ORACLE_PORT}/{oracle_config.ORACLE_SERVICE}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
