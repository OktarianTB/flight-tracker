from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, TextAreaField, DateField
from wtforms.validators import DataRequired, Length


class UpdateUserSettings(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=25)])
    submit = SubmitField("Save Changes")


class NewLocation(FlaskForm):
    name = StringField("Your Location Name", validators=[DataRequired(), Length(min=3, max=35)])
    description = TextAreaField(" Your Description", validators=[Length(min=0, max=200)])
    submit = SubmitField("Add Location")
