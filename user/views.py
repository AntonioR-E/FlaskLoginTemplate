from flask import Blueprint, render_template
import bcrypt

# local
from user.models import User
from user.forms import RegisterForm

user_app = Blueprint('user_app', __name__)

@user_app.route('/logout')
def logout():
	if'username' in session:
		session.pop('username', None)
		return redirect(url_for('index'))
	return 'You are not logged in'

@user_app.route('/login')
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects.filter(
            username=form.username.data
            ).first()
        if user:
    		 if bcrypt.hashpw(form.password.data, user.password) == user.password:
                 session['username'] = form.username.data# set the session variables
                 session['roles'] = user.roles
                 if user.active == False:
                    session.pop('username', None)
     				return "Your requested account is still under review <a href='index'> Home <a>"

    			if(login_user['roles']=='admin'):
    				return redirect(url_for('admin'))
    			return redirect(url_for('index'))

            else:
                user = None
        if not user:
            error = 'Incorrect credentials'
    return render_template('user/login.html', form=form, error=error)
@user_app.route('/register', methods=('GET','POST'))
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
