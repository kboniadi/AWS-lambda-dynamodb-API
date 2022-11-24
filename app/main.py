import os
import uuid as uuid
from datetime import date, datetime

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import (LoginManager, UserMixin, current_user, login_required,
                         login_user, logout_user)
from app.webforms import (LoginForm, NamerForm, PasswordForm, PostForm, SearchForm,
                      UserForm)
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from app import create_app

app = create_app()

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
def index():
	first_name = "John"
	stuff = "This is bold text"

	favorite_pizza = ["Pepperoni", "Cheese", "Mushrooms", 41]
	return render_template("index.html", 
		first_name=first_name,
		stuff=stuff,
		favorite_pizza = favorite_pizza)

# Create Custom Error Pages

# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html"), 404

# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
	return render_template("500.html"), 500
