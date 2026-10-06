from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, Optional


class EducationForm(FlaskForm):
    institution = StringField('Institution', validators=[DataRequired(), Length(max=150)])
    degree = StringField('Degree / Track', validators=[DataRequired(), Length(max=150)])
    location = StringField('Location', default='Algeria', validators=[DataRequired(), Length(max=100)])
    start_year = StringField('Start Year', validators=[DataRequired(), Length(max=20)])
    end_year = StringField('End Year', validators=[DataRequired(), Length(max=20)])
    grade = StringField('Grade / Mention', validators=[Optional(), Length(max=60)])
    highlights = TextAreaField('Subject Highlights (separate with | symbol)', validators=[Optional()])
    description = TextAreaField('Narrative / Details', validators=[Optional()])
    order_num = IntegerField('Order Number', default=0)
    submit = SubmitField('Save Education')
