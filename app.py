""" Para poder trabajar con tokens """
import os
""" Importar los formularios """
from forms.forms import *
""" Importar flask """
from flask import Flask, render_template, redirect, url_for
from forms.forms import BookFlightForm
""" Para conectar con la base de datos """
from db import *
""" Importar helpers """
from flask.helpers import flash

app = Flask(__name__)
""" metodo para usar el token """
app.secret_key = os.urandom(24)

@app.route('/', methods=['GET'])
def index():
    return render_template ('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ""
    form = LoginForm()
    if(form.validate_on_submit()):                
        usuario = form.usuario.data
        contrasena = form.contraseña.data
        sql = f'SELECT * FROM user WHERE usuario = "{usuario}"'
        db = get_db()
        cursorObj = db.cursor()
        cursorObj.execute(sql)       
        usuarios = cursorObj.fetchall()
        if len(usuarios) > 0:
            contrasenaHas = usuarios[0][2]
            if check_password_hash(contrasenaHas, contrasena):            
                session.clear()
                session['id'] = usuarios[0][0]
                session['user'] = usuarios[0][1]
                session['password'] = contrasenaHas            
                return redirect(url_for('index'))
            else:
                flash(f'Clave incorrecta')
                return redirect(url_for('login'))
        else:
                flash(f'El usuario ingresado no existe')             
    return render_template("login.html", form=form)

@app.route('/signUp')
def signup():
    return render_template('signup.html')

@app.route('/user/')
def user():
    return render_template('user.html')

@app.route('/bookFlight', methods=["GET", "POST"])
def bookFlight():
    form = BookFlightForm()
    return render_template('bookFlight.html', form=form)

@app.route('/selectBooking')
def selectBooking():
    sql = "SELECT * FROM Flight"
    db = get_db()
    cursorObj = db.cursor()
    cursorObj.execute(sql)
    flight = cursorObj.fetchall()
    return render_template('selectBooking.html', flight=flight)

@app.route('/searchFlight', methods=["GET", "POST"])
def searchFlight():
    form = SearchFlightForm()
    return render_template('searchFlight.html', form=form)

@app.route('/rateFlight', methods=["GET", "POST"])
def rateFlight():
    form = RateFlightForm()
    return render_template('rateFlight.html', form=form)

@app.route('/flights')
def flights():
    return render_template('flights.html')
    
@app.route('/pilot', methods=["GET", "POST"])
def pilot():
    form = SearchFlightPilotForm()
    return render_template("pilot.html",form=form)

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/addFlight', methods=['GET','POST'])
def addFlight():
    form = AddFlightForm()
    return render_template('addFlight.html', form=form)

@app.route('/addUser', methods=['GET','POST'])
def addUser():
    form = AddUserForm()
    return render_template('addUser.html', form=form)

@app.route('/manageUser', methods=['GET'])
def manageUser():
    return render_template('manageUser.html')

@app.route('/editUser', methods=['GET','POST'])
def editUser():
    form = EditUserForm()
    return render_template('editUser.html', form=form)

@app.route('/deleteUser', methods=['GET','POST'])
def deleteUser():
    form = DeleteUserForm()
    return render_template('deleteUser.html', form=form)