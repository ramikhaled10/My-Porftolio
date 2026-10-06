from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class ContactForm(FlaskForm):
    name = StringField('Your Name', validators=[
        DataRequired(message='Please provide your name.'),
        Length(min=2, max=100, message='Name must be between 2 and 100 characters.')
    ])
    email = StringField('Your Email', validators=[
        DataRequired(message='Please provide a valid email address.'),
        Email(message='Please enter a valid email address.'),
        Length(max=120)
    ])
    subject = StringField('Subject', validators=[
        DataRequired(message='Please provide a subject.'),
        Length(min=3, max=200, message='Subject must be between 3 and 200 characters.')
    ])
    message = TextAreaField('Message', validators=[
        DataRequired(message='Please write your message.'),
        Length(min=10, max=5000, message='Message must be at least 10 characters.')
    ])
    submit = SubmitField('Send Message')
