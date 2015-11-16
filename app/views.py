from flask import render_template, flash, redirect
from .forms import LoginForm

from app import app, db, models


@app.route('/')
@app.route('/index')
def index():
    user = models.User.query.get(1)

    posts = user.posts.all()
    return render_template("index.html",
                           title='Home',
                           user=user,
                           posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        flash("Login requested for OpenID=%s, remember_me=%s" % (
            form.openid.data,
            form.remember_me.data))
        return redirect('index')

    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])
