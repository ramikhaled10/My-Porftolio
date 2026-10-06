from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import Optional, Length


class SiteSettingsForm(FlaskForm):
    hero_tagline = StringField('Hero Tagline', validators=[Optional(), Length(max=255)])
    hero_bio = TextAreaField('Hero Bio', validators=[Optional()])
    status_text = StringField('Current Status Badge', validators=[Optional(), Length(max=150)])
    github_url = StringField('GitHub Profile URL', validators=[Optional(), Length(max=255)])
    linkedin_url = StringField('LinkedIn Profile URL', validators=[Optional(), Length(max=255)])
    contact_email = StringField('Contact Email', validators=[Optional(), Length(max=120)])
    submit = SubmitField('Update Settings')
