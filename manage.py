import os
from flask.ext.script import Manager

from blog import app
from blog.models import Post, User
from blog.database import session

from getpass import getpass
from werkzeug.security import generate_password_hash


manager = Manager(app)

@manager.command
def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
    
@manager.command
def seed():
    content = """Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."""

    for i in range(25):
        post = Post(
            title="Test Post #{}".format(i),
            content=content
        )
        session.add(post)
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
    



  