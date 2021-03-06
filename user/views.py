from flask import Blueprint, render_template, session, url_for, redirect, request
import bcrypt

# local
from user.models import User
from user.forms import RegisterForm, LoginForm

user_app = Blueprint('user_app', __name__)


@user_app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username', None)
        return redirect(url_for('index'))
    return 'You are not logged in'


@user_app.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    error = None

    if request.method == 'GET' and request.args.get('next'):
        session['next'] = request.args.get('next')

    if form.validate_on_submit():
        user = User.objects.filter(
            username=form.username.data
        ).first()
        if user:
            if bcrypt.hashpw(form.password.data, user.password) == user.password:
                session['username'] = form.username.data  # set the session variables
                session['role'] = user.role
                if not user.active:
                    session.pop('username', None)
                    error = 'Your account is still under review'

                if user.role == 'admin':
                    return redirect(url_for('user.profile'))

                return redirect(url_for('index'))

            else:
                user = None

        if not user:
            error = 'Incorrect credentials'

    return render_template('user/login.html', form=form, error=error)


@user_app.route('/register', methods=('GET', 'POST'))
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(form.password.data, salt)
        user = User(
            username=form.username.data,
            password=hashed_password,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data
        )
        user.save()
        return "User register"
    return render_template('user/register.html', form=form)


@user_app.route('/users', methods=['GET'])
def get_all_users():
    error = None
    message = None
    user = User.objects.filter(username=session.get('username')).first()
    if user:
        if user.role == 'Admin':
            return 'success'
        else:
            return 'fail'

    # if 'username' in session:
    #     db_users = mongo.db.user.find();
    #     if (session['roles'] == 'admin'):
    #         return render_template('users.html', db_users=db_users)
    # return "You do not have permission for this page"


# @user_app.route('/delete/<ObjectId:userid>', methods=['GET'])
# def delete_user(userid):
#     user = mongo.db.user
#     delete_this = user.find_one_or_404({'_id': userid})
#     user.remove(delete_this)
#     return 'removed'
