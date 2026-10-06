from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, BooleanField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, Optional


CATEGORY_CHOICES = [
    ('Python', 'Python Core'),
    ('Web', 'Web Development'),
    ('Automation', 'Automation & Scraping'),
    ('GUI', 'Desktop GUI'),
    ('Games', 'Interactive Games'),
    ('Data', 'Data Science & Viz'),
    ('APIs', 'API Integrations'),
    ('Mobile', 'Mobile Development (Flutter)')
]


class ProjectForm(FlaskForm):
    title = StringField('Project Title', validators=[DataRequired(), Length(max=120)])
    slug = StringField('Slug (URL Identifier)', validators=[DataRequired(), Length(max=150)])
    summary = TextAreaField('Short Summary (Homepage card)', validators=[DataRequired(), Length(max=350)])
    description = TextAreaField('Full Description', validators=[DataRequired()])
    problem = TextAreaField('Problem Statement', validators=[Optional()])
    approach = TextAreaField('Engineering Approach & Architecture', validators=[Optional()])
    key_features = TextAreaField('Key Features (one per line)', validators=[Optional()])
    key_learnings = TextAreaField('Key Takeaways & What I Learned', validators=[Optional()])
    challenges = TextAreaField('Challenges Encountered & Solutions', validators=[Optional()])
    future_improvements = TextAreaField('Future Improvements & Extensions', validators=[Optional()])
    
    category = SelectField('Category', choices=CATEGORY_CHOICES, validators=[DataRequired()])
    technologies = StringField('Technologies (comma-separated, e.g. Python, Flask, SQLite)', validators=[DataRequired(), Length(max=255)])
    
    github_url = StringField('GitHub URL (Leave blank if coming soon)', validators=[Optional(), Length(max=255)])
    demo_url = StringField('Live Demo URL', validators=[Optional(), Length(max=255)])
    image_url = StringField('Image / Cover Graphic URL', validators=[Optional(), Length(max=255)])
    
    featured = BooleanField('Feature on Homepage')
    published = BooleanField('Published (Visible to public)', default=True)
    order_num = IntegerField('Display Order', default=0)
    
    submit = SubmitField('Save Project')
