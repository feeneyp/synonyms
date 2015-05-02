import os
from flask.ext.script import Manager

from synonyms import app
from synonyms.models import Word, User
from synonyms.database import Base, session

from getpass import getpass
from werkzeug.security import generate_password_hash

from flask.ext.migrate import Migrate, MigrateCommand

manager = Manager(app)

class DB(object):
    def __init__(self, metadata):
        self.metadata = metadata

migrate = Migrate(app, DB(Base.metadata))
manager.add_command('db', MigrateCommand)

@manager.command
def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
    
@manager.command
def seed():
    content = """Lorem ipsum."""

    for i in range(10):
        word = Word(
            content=content, category="", level=""
        )
        session.add(word)
    session.commit()   
    
@manager.command
def adduser():
    user = User()
    user.name = raw_input("Name: ")
    email = raw_input("Email: ")
    if email == session.query(User).filter(User.email==email).first():
        print "Someone's already registered with that email."
        return
    user.email = email  
    password = ""
    password2 = ""
    while not (password and password2) or password != password2:
        password = getpass("Password:")
        password2 = getpass("Repeat password:")
    user.password = generate_password_hash(password)
    session.add(user)
    session.commit()

if __name__ == "__main__":
    manager.run()
    



  