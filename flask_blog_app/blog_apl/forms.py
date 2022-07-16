from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class NewPostForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    content = TextAreaField('Содержание', validators=[DataRequired()])
    lemma = TextAreaField('Краткая (до 128 символов) необязательная аннотация', validators=[Length(max=128)])
    submit = SubmitField('Post')


class CommentForm(FlaskForm):
    text = StringField('Прокомментировать:', validators=[DataRequired()])
    submit = SubmitField('Опубликовать комментарий')
