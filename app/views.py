from flask import render_template, flash, redirect, session, url_for, request
from app import app, db, models
from .website_forms import LoginForm, RegisterForm, PostForm
import datetime
import json

# Check login details by querying database
def loginDetailsCheck(u, p):
    correct_details = models.DBUsers.query.filter(models.DBUsers.username == u, models.DBUsers.password == p).first()

    if correct_details:
        return True
    else:
        return False

# Check user is logged in before accessing the page
def userLoggedIn():
    if "username" not in session:
        return False
    else:
        return True

# Check username is not already in use / user is not reusing title name
def detailsDuplicationCheck(input, register, author, dob):
    string = ""
    if register:
        details = models.DBUsers.query.filter(models.DBUsers.username == input).first()
        print("One")
        if dob > datetime.date.today():
            print(input)
            string = "Invalid date of birth"
        elif details:
            string = "Username already in use."
    else:
        details = models.DBPosts.query.filter(models.DBPosts.title == input, models.DBPosts.author_id == author).first()
        if details:
            string = "Post title already in use."

    return string


# Return all posts that have liked by a specific user
def all_post_likes(user):
    liked_posts = db.session.query(models.user_likes).filter(models.user_likes.c.user_id == user.id)
    return liked_posts


# Login Page
@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit:
        if loginDetailsCheck(form.username.data, form.password.data):
            session["username"] = form.username.data
            return redirect(url_for('homepage'))


    return render_template('login.html', title='Login', form=form)


# Register Page
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        duplicate_validation = detailsDuplicationCheck(form.username.data, True, None, form.dob.data)
        if duplicate_validation == "":
            new_user = models.DBUsers(username=form.username.data,
                                    password=form.password.data,
                                    dob=form.dob.data)
            db.session.add(new_user)
            db.session.commit()
            flash('Successfully created account. Username: %s' % (form.username.data), 'success')
            return redirect(url_for('login'))
        else:
            flash('Error: %s' % (duplicate_validation), 'danger')

    return render_template('register.html',
                           title='Register',
                           form=form)


# Log out method
@app.route('/log_out')
def logout():
	session.pop('username', None)
	return redirect(url_for('login'))


# Homepage. Displays all posts, newest first
@app.route('/homepage', methods=['GET', 'POST'])
def homepage():
    
    if not userLoggedIn():
        return redirect(url_for('login'))

    home = {'description': 'Look at all the recent posts on BlogPosts!'}
    username = session["username"]

    user = models.DBUsers.query.filter(models.DBUsers.username == username).first()
    posts = models.DBPosts.query.order_by(models.db.desc(models.DBPosts.date)).all()

    return render_template('homepage.html', title='Homepage', home=home, user=user, posts=posts)


# Liked posts. Displays all posts the user has liked
@app.route('/liked_posts', methods=['GET', 'POST'])
def liked_posts():
    
    if not userLoggedIn():
        return redirect(url_for('login'))

    home = {'description': 'All the posts that you have liked!'}
    username = session["username"]

    user = models.DBUsers.query.filter(models.DBUsers.username == username).first()
    posts = user.liked_posts

    return render_template('liked_posts.html', title='Liked Posts', home=home, user=user, posts=posts)

# View Profile page. Displays a user's posts
@app.route('/profile/<int:user_id>', methods=['GET', 'POST'])
def profile(user_id):
    
    if not userLoggedIn():
        return redirect(url_for('login'))

    home = {'description': 'Below you will find all posts from this user.'}

    username = session["username"]
    user = models.DBUsers.query.filter(models.DBUsers.username == username).first()

    author = models.DBUsers.query.filter(models.DBUsers.id == user_id).first()
    posts = models.DBPosts.query.filter(models.DBPosts.author_id == user_id)

    return render_template('profile.html', title='Profile', home=home, user=user, posts=posts, author=author)

# Create post form
@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
    if not userLoggedIn():
        return redirect(url_for('login'))

    username = session["username"]
    user = models.DBUsers.query.filter(models.DBUsers.username == username).first()

    form = PostForm()
    if form.validate_on_submit():
        duplicate_validation = detailsDuplicationCheck(form.title.data, False, user.id, None)
        if duplicate_validation == "":
            new_post = models.DBPosts(title=form.title.data,
                                    content=form.content.data,
                                    date=datetime.datetime.now())
            
            new_post.dbusers = user
            db.session.add(new_post)
            db.session.commit()
            flash('Successfully created post.', 'success')
            return redirect(url_for('homepage'))
        else:
            flash('Error: %s' % (duplicate_validation), 'danger')

    return render_template('create_post.html',
                           title='Create Post',
                           form=form)

# This function finds a record by its ID and deletes it from the database
@app.route('/delete/<int:user_id>/<int:post_id>')
@app.route('/delete/<int:user_id>')
def delete(user_id, post_id=None):

    if post_id == None:
        account = models.DBUsers.query.get(user_id)

        for post in account.liked_posts:
            post.likes -= 1

        account.posts.delete()

        db.session.delete(account)

        db.session.commit()
        return redirect(url_for('logout'))
    else:
        post = models.DBPosts.query.get(post_id)
        db.session.delete(post)
        db.session.commit()

        return redirect(url_for('profile', user_id=user_id))


# This function adds 'Likes' functionality
@app.route('/like', methods=['POST'])
def like():

    data = json.loads(request.data)
    post_id = int(data.get('post_id'))
    post = models.DBPosts.query.get(post_id)

    username = session["username"]
    user = models.DBUsers.query.filter(models.DBUsers.username == username).first()

    already_liked = db.session.query(models.user_likes).filter(models.user_likes.c.user_id == user.id, models.user_likes.c.post_id == post.id).first()
    
    if not already_liked:
        user.liked_posts.append(post)
        post.likes += 1          
        db.session.commit()
    else:
        user.liked_posts.remove(post)
        post.likes -= 1          
        db.session.commit()

    
    return json.dumps({'status':'OK','likes': post.likes })
