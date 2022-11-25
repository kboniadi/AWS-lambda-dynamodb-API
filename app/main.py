import os
import uuid as uuid
from datetime import date, datetime

from flask import Flask, flash, redirect, render_template, request, url_for, current_app
from flask_login import (LoginManager, UserMixin, current_user, login_required,
                         login_user, logout_user)
from app.webforms import (LoginForm, NamerForm, PasswordForm, PostForm, SearchForm,
                      UserForm)
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from app import create_app

from app.routers.lawyers.routes import lawyers_domain

app = create_app()

# Flask_Login Stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # type: ignore

@login_manager.user_loader
def load_user(user_id):
	return Users(current_app.config["USER_NAME"], current_app.config["PASSWORD"])

#def index():
#	return "<h1>Hello World!</h1>"

# FILTERS!!!
#safe
#capitalize
#lower
#upper
#title
#trim
#striptags

# Create a route decorator
@app.route('/')
@login_required
def index():
	first_name = "John"
	stuff = "This is bold text"

	favorite_pizza = ["Pepperoni", "Cheese", "Mushrooms", 41]
	return render_template("index.html", 
		first_name=first_name,
		stuff=stuff,
		favorite_pizza = favorite_pizza)

# Create Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = Users(current_app.config["USER_NAME"], current_app.config["PASSWORD"])
		# Check the hash
		if form.username.data == user.user_name and check_password_hash(user.password_hash, form.password.data):
			login_user(user)
			flash("Login Succesfull!!")
			return redirect(url_for('dashboard'))
		else:
			flash("Wrong Username or Password - Try Again!")

	return render_template('login.html', form=form)

# Create Logout Page
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
	logout_user()
	flash("You Have Been Logged Out!")
	return redirect(url_for('login'))

# Create Dashboard Page
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
	lawyers = lawyers_domain.get_all()
	
	if request.method == 'POST':
		btn_type, email = request.form['submit_button'].split(" ")
		if btn_type == "Edit":
			flash(f"Successfully updated the account associated with {email}")
		elif btn_type == "Delete":
			lawyers_domain.delete_lawyer(email)
			flash(f"Successfully deleted {email}")
		
		return redirect(url_for("dashboard"))


	return render_template('dashboard.html', lawyers=lawyers)


# Create Custom Error Pages

# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html"), 404

# Internal Server Error
@app.errorhandler(500)
def internal_error_page(e):
	return render_template("500.html"), 500

# Create Model
class Users(UserMixin):
	def __init__(self, user_name, password):
		self.id = 1
		self.user_name = user_name
		self.password = password

	@property
	def password(self):
		raise AttributeError('password is not a readable attribute!')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	# Create A String
	def __repr__(self):
		return '<Name %r>' % self.user_name