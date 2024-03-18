from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, TextAreaField, SubmitField, IntegerField, SelectField, FileField
from wtforms.validators import DataRequired, Email, Length


class PropertyForm(FlaskForm):
    title = StringField('Property Title', validators=[DataRequired(), Length(min=2, max=255)])
    description = TextAreaField('Description', validators=[DataRequired()])
    num_bedrooms = IntegerField('No. of Bedrooms', validators=[DataRequired()])
    num_bathrooms = IntegerField('No. of Bathrooms', validators=[DataRequired()])
    price = IntegerField('Price', validators=[DataRequired()])
    property_type = SelectField('Property Type', choices=[('House', 'House'), ('Apartment', 'Apartment')],
                                validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    photo = FileField('Photo', validators=[DataRequired(), FileAllowed(['jpg', 'jpeg', 'png'])])
