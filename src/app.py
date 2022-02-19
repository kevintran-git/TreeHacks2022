import asyncio
import atexit
from functools import wraps
import asyncpg
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import LoginManager, login_user, login_required, UserMixin, logout_user, current_user
from flask import Flask, render_template, request, flash, redirect, url_for, abort

from src.db import get_login_user

# INIT FLASK
app = Flask(__name__)

# INIT DATABASE AND ASYNC
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
app.config.from_pyfile('config.py', silent=True)
app.pool = loop.run_until_complete(asyncpg.create_pool(app.config["DATABASE_URI"]))

# INIT LOGIN MANAGER
users = {}
login_manager = LoginManager()
login_manager.login_view = '/login/'
login_manager.init_app(app)

class User(UserMixin):

    def __init__(self):
        self.type = None
        super(User, self).__init__()


@login_manager.user_loader
def user_loader(username):
    return users.get(username)


@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for("login"))


def allowed_perms(perm_list):
    def perms(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if current_user.type in perm_list:
                return func(*args, **kwargs)
            else:
                abort(401)
        return wrapper
    return perms


def shutdown():
    loop.run_until_complete(app.pool.close())


@app.route('/')
# @login_required
def index():
    return render_template('index.html')
    # return render_template('index.html', username=current_user.id)


@app.route('/donor/')
# @login_required
# @allowed_perms(['donor'])
def donor():
    return render_template('donor.html')


@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    form = request.form
    if not form:
        flash('Please check your login details and try again.')
        return redirect(url_for('login'))

    username = form.get('username')
    password = form.get('password')
    remember = form.get('remember', False)

    db_user = loop.run_until_complete(get_login_user(pool=app.pool, username=username))

    if not db_user or not check_password_hash(db_user['password'], password):
        flash('Please check your login details and try again.')
        return redirect(url_for('login'))  # if the user doesn't exist or password is wrong, reload the page

    user = User()
    user.id = username
    user.type = db_user['type']
    login_user(user=user, remember=remember)

    users[username] = user

    return redirect(url_for('index'))


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == "__main__":
    atexit.register(shutdown)
    app.run()