from flask import render_template
from app import application

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

# def index():
#     user = {'username': 'ayophoenix'}
#     return render_template('index.html', title='Home', user=user)
