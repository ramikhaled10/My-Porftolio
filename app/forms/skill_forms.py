from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

LEVEL_CHOICES = [
    ('Foundation', 'Foundation'),
    ('Developing', 'Developing'),
    ('Familiar', 'Familiar'),
    ('Exploring', 'Exploring')
]


class SkillForm(FlaskForm):
    name = StringField('Skill Name', validators=[DataRequired(), Length(max=64)])
    category_id = SelectField('Category', coerce=int, validators=[DataRequired()])
    level = SelectField('Proficiency Level', choices=LEVEL_CHOICES, validators=[DataRequired()])
    description = StringField('Short Description / Context', validators=[Optional(), Length(max=255)])
    order_num = IntegerField('Order Number', default=0)
    submit = SubmitField('Save Skill')


class SkillCategoryForm(FlaskForm):
    name = StringField('Category Name', validators=[DataRequired(), Length(max=64)])
    icon = StringField('Lucide Icon Name (e.g. code-2, database, smartphone, cpu)', default='code-2', validators=[DataRequired()])
    order_num = IntegerField('Order Number', default=0)
    submit = SubmitField('Save Category')
