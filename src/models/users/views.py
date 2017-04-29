
from flask import Blueprint

# Using blueprints

# name is unique to this file when app is running
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from werkzeug.utils import redirect

import src.models.users.errors as UserErrors
import src.models.users.decorators as user_decorators

from src.models.users.user import User

user_blueprint = Blueprint('users', __name__)


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        # Check the login is valid
        email = request.form['email']
        password = request.form['password']

        try:
            # login valid
            if User.is_login_valid(email, password):
                session['email'] = email
                # url_for gets the url in our service for a specific method
                return redirect(url_for(".user_alerts"))

        # the individual errors are created int he User.is_login_valed meth.
        except UserErrors.UserError as e:
            return e.message

    # if invalid or GET method
    return render_template("./users/login_user.jinja2")


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        # Check the login is valid

        # ask A.J. if passing unhashed passwords is safe?
        email = request.form['email']
        password = request.form['password']

        try:
            # login valid
            if User.register_user(email, password):
                session['email'] = email
                # url_for gets the url in our service for a specific method
                return redirect(url_for(".user_alerts"))

        # the individual errors are created int he User.is_login_valed meth.
        except UserErrors.UserError as e:
            return e.message

            # if invalid or GET method

    else:
        return render_template("./users/register_user.jinja2")





@user_blueprint.route('/logout')
def logout_user():
    session['email'] = None
    # No '.home' because home is the base version in the app.py
    # if home was a method in this file would need .home
    return redirect(url_for('home'))


@user_blueprint.route('/alerts')
@user_decorators.requires_login
def user_alerts():
    user = User.find_by_email(session["email"])
    alerts = user.get_alerts()
    return render_template('./users/alerts_list.jinja2', alerts=alerts)


@user_blueprint.route('/check_alers/<string:user_id>')
def check_user_alerts(user_id):
    pass


