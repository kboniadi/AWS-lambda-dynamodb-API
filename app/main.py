import os
import uuid as uuid
from datetime import date, datetime

from flask import (Flask, current_app, flash, redirect, render_template,
                   request, url_for)
from flask_login import (LoginManager, UserMixin, current_user, login_required,
                         login_user, logout_user)
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from app import create_app
from app.domain.lawyers_domain import LawyersModel
from app.routers.lawyers.routes import lawyers_domain
from app.webforms import (LawyerForm, LoginForm, NamerForm, PasswordForm,
                          PostForm, SearchForm, UserForm)
from app.helpers.languages import languagesDict
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
	return render_template('dashboard.html', lawyers=lawyers)

@app.route('/lawyer/add', methods=['GET', 'POST'])
@login_required
def add_lawyer():
	form = LawyerForm()

	if form.validate_on_submit():
		if lawyers_domain.get_lawyer(form.email.data) is not None:
			flash("That email is already taken!!")
			form.email.errors.append("email taken")
		else:
			lawyers_domain.create_lawyer(LawyersModel(
				profile_url="",
				email=form.email.data,
				name=form.name.data,
				title=form.title.data,
				description=form.description.data,
				phone=form.phone.data,
				languages=form.languages.data or [],
				location=form.location.data,
				expertise=form.expertise.data or []
			))
			flash("A new entry has been added")
			return redirect(url_for('dashboard'))

	return render_template('add_lawyer.html', form=form)

@app.route('/lawyer/edit/<string:email>', methods=['GET', 'POST'])
@login_required
def edit_lawyer(email: str):
	lawyer = lawyers_domain.get_lawyer(email)
	original_email = str(lawyer['email'])
	lawyer["profile_url"] = ""
	form = LawyerForm(expertise=lawyer["expertise"], languages=lawyer["languages"])
	if form.validate_on_submit():
		lawyer["email"] = form.email.data
		lawyer["name"] = form.name.data
		lawyer["title"] = form.title.data
		lawyer["description"] = form.description.data
		lawyer["phone"] = form.phone.data
		lawyer["languages"] = form.languages.data
		lawyer["location"] = form.location.data
		lawyer["expertise"] = form.expertise.data

		try:
			lawyers_domain.update_lawyer(LawyersModel.parse_obj(lawyer))
		except:
			raise
		else:
			if original_email != lawyer['email']:
				print("deleted")
				lawyers_domain.delete_lawyer(original_email)

		flash("Lawyer info has been updated")
		return redirect(url_for('dashboard'))

	form.email.data = lawyer["email"]
	form.name.data = lawyer["name"]
	form.title.data = lawyer["title"]
	form.description.data = lawyer["description"]
	form.phone.data = lawyer["phone"]
	form.location.data = lawyer["location"]
	return render_template('edit_lawyer.html', form=form)

@app.route('/lawyer/delete/<string:email>', methods=['GET', 'POST'])
@login_required
def delete_lawyer(email: str):
	lawyers_domain.delete_lawyer(email)
	flash(f"Successfully deleted {email}")
	return redirect(url_for("dashboard"))

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