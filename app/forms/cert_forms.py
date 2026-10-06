from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, Optional


class CertificationForm(FlaskForm):
    title = StringField('Certificate Title', validators=[DataRequired(), Length(max=150)])
    issuer = StringField('Issuing Organization', validators=[DataRequired(), Length(max=120)])
    issue_date = StringField('Date / Period', validators=[DataRequired(), Length(max=60)])
    description = TextAreaField('Description', validators=[Optional()])
    credential_url = StringField('Credential / Verification URL', validators=[Optional(), Length(max=255)])
    image_url = StringField('Certificate Image / Badge URL', validators=[Optional(), Length(max=255)])
    skills_covered = StringField('Skills Covered (comma-separated)', validators=[Optional(), Length(max=255)])
    order_num = IntegerField('Order Number', default=0)
    submit = SubmitField('Save Certification')
