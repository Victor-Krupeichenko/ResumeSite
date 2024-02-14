from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, BooleanField
from wtforms.validators import DataRequired


class ExpirienceForm(FlaskForm):
    """Форма для описания опыта"""
    year_start = IntegerField('Year Start', validators=[DataRequired()], render_kw={'placeholder': 'year_start'})
    year_finish = IntegerField('Year End', render_kw={'placeholder': 'year_finish'})
    company = StringField('Company Name', validators=[DataRequired()], render_kw={'placeholder': 'company'})
    job = StringField('Job', validators=[DataRequired()], render_kw={'placeholder': 'job'})
    description = StringField('Description', validators=[DataRequired()], render_kw={'placeholder': 'description'})
    published = BooleanField('Published', default=False)
    submit = SubmitField('Create Experience')
