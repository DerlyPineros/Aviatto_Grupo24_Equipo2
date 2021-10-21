""" Importar wtf """
from flask_wtf import FlaskForm
from wtforms.fields.core import BooleanField, DateField, SelectField, StringField, DateField, IntegerField
from wtforms import PasswordField, TextAreaField
from wtforms.validators import DataRequired

""" Crear formulario BookFlight """
class BookFlightForm(FlaskForm):
    depature = SelectField(u'Desde', validators=[DataRequired()], choices=[('1', ''),('2', 'Barranquilla'), ('3', 'Bogotá'), ('4', 'Bucaramanga'), ('5', 'Cartagena'), ('6', 'Medellín') ])
    arrival = SelectField(u'Hacia', validators=[DataRequired()], choices=[('1', ''),('2', 'Barranquilla'), ('3', 'Bogotá'), ('4', 'Bucaramanga'), ('5', 'Cartagena'), ('6', 'Medellín') ])
    depatureTime = DateField("Salida", validators=[DataRequired()], format='%d/%m/%y')
    passengers = SelectField(u'Pasajeros', validators=[DataRequired()], choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5') ])

""" Crear formulario Search Flight """
class SearchFlightForm(FlaskForm):
    idFlight = StringField(u'Código de vuelo', validators=[DataRequired()])
    depatureTime = DateField("Salida", validators=[DataRequired()], format='%d/%m/%y')

""" Crear formulario Rate Flight """
class RateFlightForm(FlaskForm):
    idFlight = IntegerField(u'Código de vuelo', validators=[DataRequired()])
    rate = SelectField(u'Calificación', validators=[DataRequired()], choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
    comment = TextAreaField(u'Comentarios', validators=[DataRequired()])

""" Crear formulario Search Flights Pilot """
class SearchFlightPilotForm(FlaskForm):
    idPilot = StringField(u'Código de piloto', validators=[DataRequired()])

""" Crear formulario Add Flights """
class AddFlightForm(FlaskForm):
    flightPlane = StringField(u'Avión', validators=[DataRequired()])
    depature = SelectField(u'Desde', validators=[DataRequired()], choices=[('1', ''),('2', 'Barranquilla'), ('3', 'Bogotá'), ('4', 'Bucaramanga'), ('5', 'Cartagena'), ('6', 'Medellín') ])
    depatureTime = DateField("Salida", validators=[DataRequired()], format='%d/%m/%y')
    capacity = IntegerField(u'Capacidad', validators=[DataRequired()])
    idPilot = StringField(u'Código de piloto', validators=[DataRequired()])

""" Crear formulario Add User """
class AddUserForm(FlaskForm):
    name = StringField(u'Nombre', validators=[DataRequired()])
    userName = StringField(u'Usuario', validators=[DataRequired()])
    emailUser= StringField(u'E-mail', validators=[DataRequired()])
    passwordUser = StringField(u'Contraseña', validators=[DataRequired()])

""" Crear formulario Edit User """
class EditUserForm(FlaskForm):
    userName = StringField(u'Usuario', validators=[DataRequired()])

""" Crear formulario Delete User """
class DeleteUserForm(FlaskForm):
    userName = StringField(u'Usuario', validators=[DataRequired()])

""" Crear formulario Login """
class LoginForm(FlaskForm):
    user = StringField('Usuario', validators=[DataRequired(message="Campo obligatorio")])
    password = PasswordField('Contraseña', validators=[DataRequired(message="Campo Obligatorio")])
    recordar = BooleanField('Recordar usuario')

""" Crear formulario Sign Up """
class SignUpForm(FlaskForm):
    name = StringField(u'Nombre', validators=[DataRequired()])
    userName = StringField(u'Usuario', validators=[DataRequired()])
    userIdtf = StringField(u'Identificación', validators=[DataRequired()])
    emailUser= StringField(u'E-mail', validators=[DataRequired()])
    passwordUser = StringField(u'Contraseña', validators=[DataRequired()])
