""" Importar wtf """
from flask_wtf import FlaskForm
from wtforms.fields.core import BooleanField, DateField, RadioField, SelectField, StringField, DateField
from wtforms.validators import DataRequired

""" Crear formulario BookFlight """
class BookFlightForm(FlaskForm):
    roundTrip = BooleanField("Ida y vuelta")
    oneWay = BooleanField("Solo ida")
    depature = SelectField(u'Desde', validators=[DataRequired()], choices=[('1', ''),('2', 'Barranquilla'), ('3', 'Bogotá'), ('4', 'Bucaramanga'), ('5', 'Cartagena'), ('6', 'Medellín') ])
    arrival = SelectField(u'Hacia', validators=[DataRequired()], choices=[('1', ''),('2', 'Barranquilla'), ('3', 'Bogotá'), ('4', 'Bucaramanga'), ('5', 'Cartagena'), ('6', 'Medellín') ])
    depatureTime = DateField("Salida", validators=[DataRequired()], format='%d/%m/%y')
    arrivalTime = DateField("Regreso", validators=[DataRequired()], format='%d/%m/%y')
    passengers = SelectField(u'Pasajeros', validators=[DataRequired()], choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5') ])

""" Crear formulario Search Flight """
class SearchFlightForm(FlaskForm):
    idFlight = StringField(u'Código de vuelo', validators=[DataRequired()])
    depatureTime = DateField("Salida", validators=[DataRequired()], format='%d/%m/%y')

""" Crear formulario Rate Flight """
class RateFlightForm(FlaskForm):
    idFlight = StringField(u'Código de vuelo', validators=[DataRequired()])

""" Crear formulario Search Flight Pilot """
class SearchFlightPilotForm(FlaskForm):
    idPilot = StringField(u'Código de piloto', validators=[DataRequired()])