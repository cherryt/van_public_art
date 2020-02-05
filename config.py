import os

class Config(object):
    user = os.getenv("SQL_USER")
    password = os.getenv("SQL_PASSWORD")
    #"postgres://wuyyggmj:pMBmfEtqqMLYM-5rH128KSFArG6dew2P@rajje.db.elephantsql.com:5432/wuyyggmj"
    TEMPLATES_AUTO_RELOAD = True
    SQLALCHEMY_DATABASE_URI = f"postgres://{user}:{password}@rajje.db.elephantsql.com:5432/{user}"
    TEMPLATES_AUTO_RELOAD = True