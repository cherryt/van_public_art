import os


class Config:
    user = os.getenv("SQL_USER")
    password = os.getenv("SQL_PASSWORD")
    TEMPLATES_AUTO_RELOAD = True
    SQLALCHEMY_DATABASE_URI = (
        f"postgres://{user}:{password}@rajje.db.elephantsql.com:5432/{user}"
    )
    TEMPLATES_AUTO_RELOAD = True
