import email
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flask_blog_app import db, bcrypt
from flask_blog_app.models import User, Post
from flask_blog_app.user_apl.forms import (
    RegForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm)
from flask_blog_app.user_apl.utilities import save_picture, send_reset_email

users = Blueprint('user_apl', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegForm()
    if form.validate_on_submit():
        print(
            f'---------\n<form.username.data> : {form.username.data}\n---------')
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Ваша учетная запись была создана!'
              ' Теперь вы можете войти в систему', 'success')
        return redirect(url_for('user_apl.login'))
        # return redirect(url_for('home.login'))
    return render_template('register.html', title='Register', form=form, current_page='Register')


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('blog_apl.postslist'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('blog_apl.postslist'))
        else:
            flash('Войти не удалось. Пожалуйста, '
                  'проверьте электронную почту и пароль', 'внимание')
    return render_template('login.html', title='Аутентификация', form=form, current_page='login')


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Ваш аккаунт был обновлен!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        page = request.args.get('page', 1, type=int)
        user = User.query.filter_by(username=form.username.data).first_or_404()
        posts = Post.query.filter_by(author=user) \
            .order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    image_file = url_for(
        'static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form, posts=posts, user=user, current_page='account')


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/bloger/<string:blogername>")
def bloger_posts(blogername):
    page = request.args.get('page', 1, type=int)
    bloger = User.query.filter_by(username=blogername).first_or_404()
    posts = Post.query.filter_by(author=bloger).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=bloger, current_page='bloger_posts')


@users.route("/reset_password", methods=['GET', 'POST'])
def passwd_reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('blog_apl.postslist'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('На почту отправлено письмо с инструкциями по сбросу пароля.', 'info')
        return redirect(url_for('user_apl.login'))
    return render_template('reset_request.html', title='Сброс пароля', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('blog_apl.postslist'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Это недействительный или просроченный токен', 'warning')
        return redirect(url_for('user_apl.passwd_reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_passwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_passwd
        db.session.commit()
        flash('Ваш пароль был обновлён! Теперь вы можете авторизоваться', 'success')
        return redirect(url_for('user_apl.login'))
    return render_template('reset_token.html', title='Сброс пароля', form=form)
