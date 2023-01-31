from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired


class UploadForm(FlaskForm):
    fileName = FileField('Upload File', validators=[DataRequired()])
    submit = SubmitField('Extract')
