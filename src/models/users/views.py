
from flask import Blueprint

# Using blueprints

# name is unique to this file when app is running
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from werkzeug.utils import redirect

import src.models.users.errors as UserErrors
from src.models.users.user import User

user_blueprint = Blueprint('users', __name__)


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        # Check the login is valid
        email = request.form['email']
        password = request.form['hashed']

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
    return render_template("user/login.html")


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        # Check the login is valid
        email = request.form['email']
        password = request.form['hashed']

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
    return render_template("user/register.html")


@user_blueprint.route('/alerts')
def user_alerts():
    return "This is the alerts page."


@user_blueprint.route('/logout')
def logout_user():
    pass

@user_blueprint.route('/check_alers/<string:user_id>')
def check_user_alerts(user_id):
    pass