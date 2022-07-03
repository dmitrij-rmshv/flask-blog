from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def eroor_404(error):
    return render_template('errors/404.html', current_page='error'), 404


@errors.app_errorhandler(403)
def eroor_404(error):
    return render_template('errors/403.html', current_page='error'), 403


@errors.app_errorhandler(500)
def eroor_500(error):
    return render_template('errors/500.html', current_page='error'), 500
