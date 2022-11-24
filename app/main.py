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
login_manager.login_view = 'login'

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
	print(lawyers)
	# form = UserForm()
	# if request.method == "POST":
	# 	name_to_update.name = request.form['name']
	# 	name_to_update.email = request.form['email']
	# 	name_to_update.favorite_color = request.form['favorite_color']
	# 	name_to_update.username = request.form['username']
	# 	name_to_update.about_author = request.form['about_author']
		

	# 	# Check for profile pic
	# 	if request.files['profile_pic']:
	# 		name_to_update.profile_pic = request.files['profile_pic']

	# 		# Grab Image Name
	# 		pic_filename = secure_filename(name_to_update.profile_pic.filename)
	# 		# Set UUID
	# 		pic_name = str(uuid.uuid1()) + "_" + pic_filename
	# 		# Save That Image
	# 		saver = request.files['profile_pic']
			

	# 		# Change it to a string to save to db
	# 		name_to_update.profile_pic = pic_name
	# 		try:
	# 			db.session.commit()
	# 			saver.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))
	# 			flash("User Updated Successfully!")
	# 			return render_template("dashboard.html", 
	# 				form=form,
	# 				name_to_update = name_to_update)
	# 		except:
	# 			flash("Error!  Looks like there was a problem...try again!")
	# 			return render_template("dashboard.html", 
	# 				form=form,
	# 				name_to_update = name_to_update)
	# 	else:
	# 		db.session.commit()
	# 		flash("User Updated Successfully!")
	# 		return render_template("dashboard.html", 
	# 			form=form, 
	# 			name_to_update = name_to_update)
	# else:
	# 	return render_template("dashboard.html", 
	# 			form=form,
	# 			name_to_update = name_to_update,
	# 			id = id)

	return render_template('dashboard.html')


# Create Custom Error Pages

# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html"), 404

# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
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