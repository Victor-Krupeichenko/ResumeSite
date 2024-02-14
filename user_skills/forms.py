from flask_wtf import FlaskForm
from wtforms import StringField, FileField, SubmitField
from wtforms.fields.simple import BooleanField
from wtforms.validators import DataRequired


class SkillForm(FlaskForm):
    """
    Форма добавления навыка
    """
    title = StringField('Title', validators=[DataRequired()], render_kw={"placeholder": "title"})
    img = FileField('Image', default=None)
    description = StringField('Description', validators=[DataRequired()], render_kw={"placeholder": "description"})
    published = BooleanField('Published', default=False)
    submit = SubmitField('add skills')
