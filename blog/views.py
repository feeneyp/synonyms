import mistune
from flask import render_template, request, redirect, url_for
from flask import flash
from flask.ext.login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash

from blog import app 
from .database import session
from .models import Post
from .models import User



@app.route("/")
def posts():
    posts = session.query(Post)
    posts = posts.order_by(Post.datetime.desc())
    posts = posts.all()
    return render_template("posts.html",
        posts=posts
    )
  
@app.route("/post/<id>")
def post_get(id):
    post = session.query(Post).get(id)
    return render_template("post.html",post=post)  
  
@app.route("/post/add", methods=["GET"]) #button u click is in posts.html
@login_required
def add_post_get():
    return render_template("add_post.html")  
  

@app.route("/post/add", methods=["POST"]) #button u click is in add_post.html
@login_required
def add_post_post():
    post = Post(
      title=request.form["title"],
      content=mistune.markdown(request.form["content"]), 
      author=current_user
    )
    session.add(post)
    session.commit()
    return redirect(url_for("posts"))

  
@app.route("/post/<id>/edit", methods=["GET"])
@login_required
def edit_post_get(id):
    post=session.query(Post).get(id)
    if current_user.id == post.author_id:
        return render_template("edit_post.html", post=post)
    else:
        flash("You cannot edit other users' posts.","danger")
        return redirect(url_for("posts"))
  
  
@app.route("/post/<id>/edit", methods=["POST"])
@login_required
def edit_post_post(id):
    post=session.query(Post).get(id)
    post.title=request.form["title"]
    post.content=mistune.markdown(request.form["content"])
    session.commit()
    return redirect(url_for("posts"))
  
@app.route("/post/<id>/delete", methods=["GET"])
@login_required
def delete_post_get(id):
    post=session.query(Post).get(id)
    return render_template("delete_post.html", post=post)
  
@app.route("/post/<id>/delete", methods=["POST"])
@login_required
def delete_post_post(id):
    post=session.query(Post).get(id)
    session.delete(post)
    session.commit()
    return redirect(url_for("posts"))
  
@app.route("/login", methods=["GET"])
def login_get():
    if not current_user.is_authenticated():
        return render_template("login.html")
    else:
        flash("You are currently logged in.  To login another user, please log out.", "info")
        return redirect(url_for("posts"))
  
@app.route("/login", methods=["POST"])
def login_post():
    email = request.form["email"]
    password = request.form["password"]
    #at end of line below this one you need to have first() otherwise returns list
    user = session.query(User).filter(User.email==email).first() 
    if not user or not check_password_hash(user.password, password):
        flash("Incorrect username or password", "danger")
        return redirect(url_for("login_get"))
    login_user(user)
    return redirect(request.args.get('next') or url_for("posts"))

@app.route("/logout")
def logout():
    if current_user.is_authenticated():
        flash("You have been logged out.","info")
        logout_user()
        return redirect(url_for("login_get"))
    else:    
        flash("You cannot logout.  You are not logged in.  Please log in.", "danger")
        return redirect(url_for("login_get"))    
