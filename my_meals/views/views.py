from functools import wraps
from flask import g, request, redirect, url_for, flash, session, render_template

from my_meals.main import app
from my_meals.models import User
from my_meals.forms import MemberForm


def get_user_role():
    return g.user.role if g.user else None


def required_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if get_user_role() not in roles:
                flash('You have no privileges to do this action!', 'danger')
                return redirect(url_for('home'))
            return f(*args, **kwargs)
        return wrapped
    return wrapper


@app.before_request
def _before_request():
    if session.get('logged_in'):
        username = session['logged_in']
        g.user = User.query.filter_by(username=username).first()
        return

    if 'static' in request.url:
        return
    
    if 'register' in request.url:
        return

    if 'login' in request.url and request.method == 'GET':
        return

    if 'logged_in' not in session and 'login' not in request.url:
        return redirect(url_for('login', next=request.url))


@app.errorhandler(404)
def page_not_found():
    return render_template('404.html', user=g.user), 404


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['inputUsername']
        password = request.form['inputPassword']
        user = User.query.filter_by(username=username).first()
        
        if user is None:
            flash('No user found', 'danger')
            return redirect('login')

        if not user.check_password(password):
            flash('Wrong password, try again!', 'danger')
            return redirect('login')

        else:
            session['logged_in'] = username
            return redirect(url_for('home'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    member_form = MemberForm(request.form)
    if request.method == 'POST' and member_form.validate():
        username = member_form.username.data
        password = member_form.password.data
        user = User(username, password, 'user')
        user.save()
        flash('You were successfully registred. Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=member_form)


@app.route('/')
def home():
    return render_template('meals.html', user=g.user)


@app.route('/users')
@required_roles('admin', 'user_manager')
def users():
    return render_template('users.html', user=g.user)


@app.route('/admin')
@required_roles('admin')
def admin_page():
    users = User.query.filter_by(role='user').all()
    return render_template('admin.html', users=users, user=g.user)


@app.route('/profile/<username>')
@required_roles('admin')
def profile(username):
    if g.user.username == username: return redirect('/')
    user = User.query.filter_by(username=username).first()
    if not user: return render_template('404.html', user=g.user), 404
    return render_template('profile.html', user=g.user, username=user.username)
