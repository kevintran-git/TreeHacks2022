import asyncio
import atexit
from functools import wraps
import asyncpg
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import LoginManager, login_user, login_required, UserMixin, logout_user, current_user
from flask import Flask, render_template, request, flash, redirect, url_for, abort

from src.db import get_login_user, get_distributor_posts, add_post, get_event_posts, acceptEvent, get_consumer_posts, \
    publishEvent

from src.forms import PostForm, AcceptForm, PublishForm

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
def index():
    return render_template('index.html')
    # return render_template('index.html', username=current_user.id)


@app.route('/event/')
@login_required
# @allowed_perms(['event'])
def eventhost():
    return render_template('eventhost.html')


@app.route('/event_post/', methods=['GET', 'POST'])
@login_required
# @allowed_perms(['event'])
def event_post():
    post = PostForm(request.form)

    if request.method == 'GET' or not post.validate():
        return redirect(url_for('event'))

    loop.run_until_complete(add_post(pool=app.pool, post=post, type='event', login=current_user.id))

    return redirect(url_for('eventhost'))


@app.route('/distributor/')
@login_required
# @allowed_perms(['distributor'])
def distributor():
    posts, accepted_posts= loop.run_until_complete(get_distributor_posts(pool=app.pool, login=current_user.id))

    return render_template('distributor.html', posts=posts, accepted_posts=accepted_posts)


@app.route('/distributor/find/')
@login_required
# @allowed_perms(['distributor'])
def distributor_find():
    posts = loop.run_until_complete(get_event_posts(pool=app.pool))

    return render_template('distributor_find.html', posts=posts)


@app.route('/distributor/post/')
@login_required
# @allowed_perms(['distributor'])
def distributor_post():
    return render_template('distributor_post.html')


@app.route('/distributor_post/', methods=['GET', 'POST'])
@login_required
# @allowed_perms(['distributor'])
def distributorPost():
    post = PostForm(request.form)

    if request.method == 'GET' or not post.validate():
        return redirect(url_for('distributor'))

    loop.run_until_complete(add_post(pool=app.pool, post=post, type='distributor', login=current_user.id))

    return redirect(url_for('distributor'))


@app.route('/accept_event/', methods=['GET', 'POST'])
@login_required
# @allowed_perms(['event'])
def accept_event():
    data = AcceptForm(request.form)

    if request.method == 'GET' or not data.validate():
        return redirect(url_for('distributor_find'))

    id = data.id.data

    loop.run_until_complete(acceptEvent(pool=app.pool, id=id, login=current_user.id))

    return redirect(url_for('distributor_find'))


@app.route('/publish_event/', methods=['GET', 'POST'])
@login_required
# @allowed_perms(['event'])
def publish_event():
    data = PublishForm(request.form)

    if request.method == 'GET' or not data.validate():
        return redirect(url_for('distributor'))

    id = data.id.data

    loop.run_until_complete(publishEvent(pool=app.pool, id=id))

    return redirect(url_for('distributor'))


@app.route('/consumer/')
# @allowed_perms(['consumer'])
def consumer():
    posts = loop.run_until_complete(get_consumer_posts(pool=app.pool))

    return render_template('consumer.html', posts=posts)


@app.route('/who_we_are/')
def who_we_are():
    return render_template('who_we_are.html')


@app.route('/our_mission/')
def our_mission():
    return render_template('our_mission.html')


@app.route('/contact_us/')
def contact_us():
    return render_template('contact_us.html')


@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    form = request.form
    if not form:
        flash('Please check your login details and try again.')
        return redirect(url_for('login'))

    login = form.get('login')
    password = form.get('password')
    remember = form.get('remember', False)

    db_user = loop.run_until_complete(get_login_user(pool=app.pool, username=login))

    if not db_user or not check_password_hash(db_user['password'], password):
        flash('Please check your login details and try again.')
        return redirect(url_for('login'))  # if the user doesn't exist or password is wrong, reload the page

    user = User()
    user.id = login
    user.type = db_user['type']
    login_user(user=user, remember=remember)

    users[login] = user

    return redirect(url_for('index'))


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == "__main__":
    atexit.register(shutdown)
    app.run()