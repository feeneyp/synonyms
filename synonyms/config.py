import os
class DevelopmentConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://action:action@localhost:5432/wordful"
    DEBUG = True
    SECRET_KEY = "Not secret"
    #used to be the line below
#     SECRET_KEY = os.environ.get("BLOGFUL_SECRET_KEY", "")
    
class TestingConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://action:action@localhost:5432/wordful-test"
    DEBUG = False
    SECRET_KEY = "Not secret"