from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, SelectField
from wtforms.validators import DataRequired


class AlgoInputForm(FlaskForm):
    items = StringField('Items (input example: ABCD)', validators=[DataRequired()])
    preferences_a = StringField('Preferences for Agent A (input example: 7432)', validators=[DataRequired()])
    preferences_b = StringField('Preferences for Agent B (input example: 1732)', validators=[DataRequired()])
    algorithm = SelectField('Algorithm',choices=['undercut'])
    submit = SubmitField('Compute')
