from flask import render_template, flash, redirect, url_for
from app import application
from app.forms import LoginForm

@application.route('/')
@application.route('/index')
def index():
    user = {'username': 'ayophoenix'}
    posts = [
        {
            'id': {'username': 'user_1'},
            'body': 'body_1'
        },
        {
            'id': {'username': 'user_2'},
            'body': 'body_2'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)

@application.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)