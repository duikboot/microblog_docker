from datetime import datetime

from flask import (render_template, flash, redirect, session, url_for,
                   request, g)
from flask.ext.login import (login_user, logout_user, current_user,
                             login_required)

from app import app, db, lm
from .forms import LoginForm
from .models import User
from .oauth import OAuthSignIn


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/')
@app.route('/index')
@login_required
def index():
    user = g.user

    posts = [
        {'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'},
        {'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'}
    ]

    return render_template('index.html',
                           title='home',
                           posts=posts,
                           user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():

    return render_template('login.html')


@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('login'))

    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email, profile_image = oauth.callback()
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('login'))

    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        user = User(social_id=social_id, nickname=username, email=email,
                    profile_image=profile_image)
        db.session.add(user)
        db.session.commit()
    login_user(user, True)
    return redirect(url_for('index'))


@app.route('/user/<nickname>')
@login_required
def user(nickname):
    user = User.query.filter_by(nickname=nickname).first()

    posts = [{"author": user, "body": "Test"}]

    return render_template("user.html", user=user, posts=posts)
