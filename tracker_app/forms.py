from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length


class UpdateUserSettings(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=25)])
    submit = SubmitField("Save Changes")


class NewLocation(FlaskForm):
    name = StringField("Your Location Name", validators=[DataRequired(), Length(min=3, max=35)])
    description = TextAreaField("Your Description", validators=[Length(min=0, max=100)])
    pin_color = SelectField("Color of Location Pin", validators=[DataRequired()], default="red",
                            choices=[("red", "Red"), ("blue", "Blue"), ("green", "Green"), ("yellow", "Yellow"),
                                     ("pink", "Pink"), ("orange", "Orange"), ("purple", "Purple")])
    submit = SubmitField("Add Location")
