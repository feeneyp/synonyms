import mistune
from flask import render_template, request, redirect, url_for

from blog import app 
from .database import session
from .models import Post

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
def add_post_get():
    return render_template("add_post.html")

@app.route("/post/add", methods=["POST"]) #button u click is in add_post.html
def add_post_post():
    post = Post(
      title=request.form["title"],
      content=mistune.markdown(request.form["content"]),
    )
    session.add(post)
    session.commit()
    return redirect(url_for("posts"))

  
@app.route("/post/<id>/edit", methods=["GET"])
def edit_post_get(id):
    post=session.query(Post).get(id)
    return render_template("edit_post.html", post=post)  
  
  
@app.route("/post/<id>/edit", methods=["POST"])
def edit_post_post(id):
    post=session.query(Post).get(id)
    post.title=request.form["title"]
    post.content=mistune.markdown(request.form["content"])
    session.commit()
    return redirect(url_for("posts"))
  
@app.route("/post/<id>/delete", methods=["GET"])
def delete_post_get(id):
    post=session.query(Post).get(id)
    return render_template("delete_post.html", post=post)
  
@app.route("/post/<id>/delete", methods=["POST"])
def delete_post_post(id):
    post=session.query(Post).get(id)
    session.delete(post)
    session.commit()
    return redirect(url_for("posts"))   