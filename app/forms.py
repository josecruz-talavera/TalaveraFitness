from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email


class ContactForm(FlaskForm):
    name = StringField(
        "Name: ", render_kw={"class": "big-textbox"}, validators=[DataRequired()]
    )
    email = StringField("Email: ", validators=[DataRequired(), Email()])
    message = TextAreaField("Message: ", validators=[DataRequired()])
    submit = SubmitField("Send")
