""" Importar wtf """
from flask_wtf import FlaskForm
from wtforms.fields.core import BooleanField, DateField, RadioField, SelectField, StringField, DateField
from wtforms.validators import Required
from wtforms.widgets.core import CheckboxInput

""" Crear formulario BookFlight """
class BookFlightForm(FlaskForm):
    completeway = BooleanField("Ida y vuelta",validators=[Required("Campo requerido")])
    oneway = BooleanField("Solo ida",validators=[Required("Campo requerido")])
    fromway = SelectField(u'Desde', validators=[Required()], choices=[('1', ''),('2', 'Barranquilla'), ('3', 'Bogotá'), ('4', 'Bucaramanga'), ('5', 'Cartagena'), ('6', 'Medellín') ])
    toway = SelectField(u'Hacia', validators=[Required()], choices=[('1', ''),('2', 'Barranquilla'), ('3', 'Bogotá'), ('4', 'Bucaramanga'), ('5', 'Cartagena'), ('6', 'Medellín') ])
    departuredate = DateField("Salida", validators=[Required()], format='%d/%m/%y', description = 'Time depature')
    returndate = DateField("Regreso", validators=[Required()], format='%d/%m/%y', description = 'Time arrival')
    passengers = SelectField(u'Pasajeros', validators=[Required()], choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5') ])

