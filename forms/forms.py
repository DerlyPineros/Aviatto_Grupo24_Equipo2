""" Importar wtf """
from flask_wtf import FlaskForm
from wtforms.fields.core import BooleanField, DateField, SelectField, StringField, DateField, IntegerField
from wtforms import PasswordField, TextAreaField
from wtforms.validators import DataRequired

""" Crear formulario BookFlight """
class BookFlightForm(FlaskForm):
    depature = SelectField(u'Desde', validators=[DataRequired()], choices=[('1', ''),('Barranquilla', 'Barranquilla'), ('Bogotá', 'Bogotá'), ('Bucaramanga', 'Bucaramanga'), ('Cartagena', 'Cartagena'), ('Medellín', 'Medellín') ])
    arrival = SelectField(u'Hacia', validators=[DataRequired()], choices=[('1', ''),('Barranquilla', 'Barranquilla'), ('Bogotá', 'Bogotá'), ('Bucaramanga', 'Bucaramanga'), ('Cartagena', 'Cartagena'), ('Medellín', 'Medellín') ])
    depatureTime = DateField("Salida", validators=[DataRequired()], format='%d/%m/%y')
    passengers = SelectField(u'Pasajeros', validators=[DataRequired()], choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5') ])

""" Crear formulario Search Flight """
class SearchFlightForm(FlaskForm):
    idFlight = IntegerField(u'Código de vuelo', validators=[DataRequired()])

""" Crear formulario Rate Flight """
class RateFlightForm(FlaskForm):
    idFlight = IntegerField(u'Código de vuelo', validators=[DataRequired()])
    rate = SelectField(u'Calificación', validators=[DataRequired()], choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
    comment = TextAreaField(u'Comentarios', validators=[DataRequired()])

""" Crear formulario Search Flights Pilot """
class SearchFlightPilotForm(FlaskForm):
    idPerson = IntegerField(u'Código de piloto', validators=[DataRequired()])

""" Crear formulario Add Flights """
class AddFlightForm(FlaskForm):
    depature = SelectField(u'Desde', validators=[DataRequired()], choices=[('1', ''),('Barranquilla', 'Barranquilla'), ('Bogotá', 'Bogotá'), ('Bucaramanga', 'Bucaramanga'), ('Cartagena', 'Cartagena'), ('Medellín', 'Medellín') ])
    arrival = SelectField(u'Hacia', validators=[DataRequired()], choices=[('1', ''),('Barranquilla', 'Barranquilla'), ('Bogotá', 'Bogotá'), ('Bucaramanga', 'Bucaramanga'), ('Cartagena', 'Cartagena'), ('Medellín', 'Medellín') ])
    depatureTime = DateField("Salida", validators=[DataRequired()], format='%d/%m/%y')
    arrivalTime = DateField("Llegada", validators=[DataRequired()], format='%d/%m/%y')
    plane = StringField(u'Aeronave', validators=[DataRequired()])
    capacity = IntegerField(u'Capacidad', validators=[DataRequired()])
    idStatus = SelectField(u'Desde', validators=[DataRequired()], choices=[('1', 'A tiempo'),('2', 'Retrasado'), ('3', 'Aterrizado'), ('4', 'Despegado')])
    idPerson = IntegerField(u'Código de piloto', validators=[DataRequired()])

""" Crear formulario Add User """
class AddUserForm(FlaskForm):
    user = StringField(u'Usuario', validators=[DataRequired()])
    password = StringField(u'Contraseña', validators=[DataRequired()])
    name = StringField(u'Nombre', validators=[DataRequired()])
    identification = IntegerField(u'Identificación', validators=[DataRequired()])
    email = StringField(u'E-mail', validators=[DataRequired()])

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
    user = StringField(u'Usuario', validators=[DataRequired()])
    password = StringField(u'Contraseña', validators=[DataRequired()])
    name = StringField(u'Nombre', validators=[DataRequired()])
    identification = IntegerField(u'Identificación', validators=[DataRequired()])
    email = StringField(u'E-mail', validators=[DataRequired()])

""" Crear formulario Add Pilot """
class AddPilotForm(FlaskForm):
    user = StringField(u'Usuario', validators=[DataRequired()])
    password = StringField(u'Contraseña', validators=[DataRequired()])
    name = StringField(u'Nombre', validators=[DataRequired()])
    identification = IntegerField(u'Identificación', validators=[DataRequired()])
    email = StringField(u'E-mail', validators=[DataRequired()])