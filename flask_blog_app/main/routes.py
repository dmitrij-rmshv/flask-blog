from flask import render_template, Blueprint
from flask_blog_app.models import User

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    return render_template('home.html', current_page='home')

@main.route("/examples")
def examples():
    return render_template('examples.html')

# @main.route("/page")
# def page():
#     return render_template('page.html')

@main.route("/another_page")
def another_page():
    return render_template('another_page.html')

@main.route("/contact")
def contact():
    return render_template('contact.html')
