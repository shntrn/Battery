from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError, IntegerField, SelectField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Length
from batteryapp.models import Battery


class NewBatteryForm(FlaskForm):
    battery_num = IntegerField('Battery Number', validators=[DataRequired()])
    submit = SubmitField('Add battery')

    def validatebattery(self, battery_num):
        battery = Battery.query.filter_by(battery_num=battery_num.data).first()
        if battery is not None:
            raise ValidationError('The Number is already exist, please use different number')


class ChangeBatteryStatusForm(FlaskForm):
    # NewBatteryForm.battery_num
    battery_num = IntegerField('Battery Number', validators=[DataRequired()])
    status = SelectField("Status: ", validators=[DataRequired()], choices=[
        (2, "Ready"),
        (3, "In-Use"),
        (4, "Charge "),
        (5, "Refresh"),
        (6, "Break-In"),
        (7, "Disposed ")])
    capacity = IntegerField("Capacity:", validators=[DataRequired()])
    room = StringField('Room', validators=[DataRequired(), Length(min=3, max=5)], default='310')
    submit = SubmitField('Change Battery Status')
