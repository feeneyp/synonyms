import mistune
from flask import render_template, request, redirect, url_for
from flask import flash
from flask.ext.login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash

from synonyms import app 
from .database import session
from .models import Word
from .models import User



@app.route("/")
def words():
    words = session.query(Word)
    words = words.order_by(Word.datetime.desc())
    words = words.all()
    return render_template("words.html", posts=words)
  
 
@app.route("/words", methods=["GET"])
def words_get_with_filter():
    """ Get a list of words"""
    # Get the querystring arguments if any
    category_like = request.args.get("category_like")
    level_like = request.args.get("level_like")
    title_like = request.args.get("title_like")
    print title_like
    # Get and filter the posts from the database
    words = session.query(Word)
#     if category_like or level_like or title_like:
#         words = words.filter(Word.category.contains(category_like))
#         words = words.filter(Word.level.contains(level_like))
    words = words.filter(Word.title.contains(title_like))
    words = words.all()
    return render_template("words.html", posts=words)

@app.route("/search", methods=["POST"])
def words_search():
    """ Get search terms and reload words"""
    search_term = request.form["search_box"]
    search_url = "/words?" + "title_like=" + search_term
    return redirect(search_url)
    
    
  
@app.route("/word/<id>/pair", methods=["GET"])
def word_pair_get(id):
    word = session.query(Word).get(id)
    posts = session.query(Word).all()
    return render_template("pair_filter.html", word=word, posts=posts)  
  
@app.route("/word/<id>/pair", methods=["POST"])
def word_pair_post(id):
    new_paired_words = request.form.getlist("new_paired_words") #request checkbox values (a list of id's)
    #convert list of str to list of integers
    new_paired_words = map(int, new_paired_words)
    #convert list of word id's to list of word objects
    #to pair two words you need two word objects.  Since my checkbox results are id's I need to iterate.. 
    word = session.query(Word).get(id)
    list = word.right_nodes
    for i in new_paired_words:
        word_object = session.query(Word).get(i)
        list.append(word_object)
    all_paired_words = list
    print  all_paired_words
    #create the association of the main word with each of the other word objects from the list
    word = session.query(Word).get(id)
    word.right_nodes = all_paired_words
    session.commit()
    return render_template("pair_filter.html", word=word, posts=posts)  
  
  
@app.route("/post/<id>")
def post_get(id):
    post = session.query(Word).get(id)
    return render_template("word.html", post=post)  
  
@app.route("/post/add", methods=["GET"]) #button u click is in words.html
@login_required
def add_post_get():
    return render_template("add_post.html")  
  

@app.route("/post/add", methods=["POST"]) #button u click is in add_post.html
@login_required
def add_post_post():
    post = Word(
      title = request.form["title"],
      content = mistune.markdown(request.form["content"]),
      category = mistune.markdown(request.form["category"]),
      level = mistune.markdown(request.form["level"]),
      author = current_user
    )
    session.add(post)
    session.commit()
    return redirect(url_for("words"))

  
@app.route("/post/<id>/edit", methods=["GET"])
@login_required
def edit_post_get(id):
    post=session.query(Word).get(id)
    if current_user.id == post.author_id:
        return render_template("edit_post.html", post=post)
    else:
        flash("You cannot edit other users' posts.","danger")
        return redirect(url_for("words"))
  
  
@app.route("/post/<id>/edit", methods=["POST"])
@login_required
def edit_post_post(id):
    post = session.query(Word).get(id)
    post.title = request.form["title"]
    post.content = request.form["content"]
    session.commit()
    return redirect(url_for("words"))
  
@app.route("/post/<id>/delete", methods=["GET"])
@login_required
def delete_post_get(id):
    post=session.query(Word).get(id)
    return render_template("delete_post.html", post=post)
  
@app.route("/post/<id>/delete", methods=["POST"])
@login_required
def delete_post_post(id):
    post=session.query(Word).get(id)
    session.delete(post)
    session.commit()
    return redirect(url_for("words"))


  
  
  
  
@app.route("/login", methods=["GET"])
def login_get():
    if not current_user.is_authenticated():
        return render_template("login.html")
    else:
        flash("You are currently logged in.  To login another user, please log out.", "info")
        return redirect(url_for("words"))
  
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
    print current_user.is_authenticated #this is see if current_user.is_athenticated is a method or property
    if current_user.is_authenticated():
        flash("You have been logged out.","info")
        logout_user()
        return redirect(url_for("login_get"))
    else:    
        flash("You cannot logout.  You are not logged in.  Please log in.", "danger")
        return redirect(url_for("login_get"))    
