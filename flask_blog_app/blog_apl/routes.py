from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required

from flask_blog_app import db
from flask_blog_app.models import Post
from flask_blog_app.blog_apl.forms import NewPostForm

posts = Blueprint('blog_apl', __name__)
print(f'-----\nBlueprint("blog_apl", __name__) :   {__name__}\n------')


@posts.route("/allposts")
@login_required
def postslist():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('allpost.html', posts=posts, current_page='allposts')


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = NewPostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Ваш пост создан', 'success')
        return redirect(url_for('blog_apl.postslist'))
    return render_template('create_post.html', title='Новый пост', form=form, legend='Новый пост', current_page='Редактирование')


@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post, current_page='post')


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def post_update(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = NewPostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Ваш пост отредактирован', 'success')
        return redirect(url_for('blog_apl.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Обновление поста', form=form, legend='Обновление поста', current_page='reduction')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Пост удалён!', 'success')
    return redirect(url_for('blog_apl.postslist'))
