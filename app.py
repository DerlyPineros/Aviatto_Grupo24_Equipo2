""" Para trabajar con tokens """
import os
""" from typing_extensions import Required """
""" Importar los formularios """
from forms.forms import *
""" Importar flask """
from flask import Flask, render_template, redirect, url_for, request
from forms.forms import BookFlightForm
""" Para conectar con la base de datos """
from db import *
""" Importar helpers """
from flask.helpers import flash
""" Importar Hash """
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
""" metodo para usar el token """
app.secret_key = os.urandom(24)

@app.route('/', methods=['GET'])
def index():
    return render_template ('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if(form.validate_on_submit()):                
        db = get_db()
        user = form.user.data
        password = form.password.data
        cursorObj = db.cursor()
        cursorObj.execute('SELECT * FROM Person WHERE user = ? and password = ?', (user, password))
        users = cursorObj.fetchall()
        if len(user) >0:
            flash(f'Bienvenido(a) {user}')
            return redirect(url_for('index'))
        else:
            flash(f'Usuario o clave inválida')
            return redirect(url_for('login'))
    return render_template("login.html", form=form)

@app.route('/signUp', methods=['GET', 'POST'])
def signUp():
    form = SignUpForm()
    if request.method == 'POST':
        Name = request.form['Name']
        userName = request.form['userName']
        userIdtf = request.form['userIdtf']
        emailUser = request.form['emailUser']
        passwordUser = request.form['passwordUser']
        passwordUserHas = generate_password_hash(passwordUser)
        sql = 'INSERT INTO Person (user, password) VALUES (?, ?) AND INSERT INTO Info (name, identification, email) VALUES (?, ?, ?)'
        db = get_db()
        result = db.execute(sql, (user, passwordUserHas,)).rowcount
        db.commit()
        if result!=0:
            flash('Registro exitoso')
        else:
            flash('Woops! Hubo un error. Intenta nuevamente')
    return render_template('signUp.html', form=form)
        flash(f'Bienvenido(a) {user}')
        return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route('/signUp')
def signup():
    form = AddUserForm()

@app.route('/user/')
def user():
    return render_template('user.html')

@app.route('/bookFlight')
def bookFlight():
    form = BookFlightForm()
    sql = "SELECT * FROM Flight"
    db = get_db()
    cursorObj = db.cursor()
    cursorObj.execute(sql)
    flight = cursorObj.fetchall()
    return render_template('bookFlight.html',form=form, flight=flight)

@app.route('/searchFlight', methods=["GET", "POST"])
def searchFlight():
    form = SearchFlightForm()
    sql = "SELECT * FROM Flight INNER JOIN Status ON Status.name = Flight.idStatus"
    db = get_db()
    cursorObj = db.cursor()
    cursorObj.execute(sql)
    flight = cursorObj.fetchall()
    return render_template('searchFlight.html', form=form, flight=flight)

@app.route('/rateFlight', methods=["GET", "POST"])
def rateFlight():
    form = RateFlightForm()
    if request.method == 'POST':
        idFlight = request.form['idFlight']
        rate = request.form['rate']
        comment = request.form['comment']
        db = get_db()
        db.execute('INSERT INTO Rate (idFlight, rate, comment) VALUES(?,?,?)',(idFlight, rate, comment))
        db.commit()
        mensajeExitoso = "Haz enviado una calificación"
        return redirect(url_for('rateFlight', mensajeExitoso=mensajeExitoso))
    return render_template('rateFlight.html', form=form)

@app.route('/flights')
def flights():
    return render_template('flights.html')
    
@app.route('/pilot', methods=["GET", "POST"])
def pilot():
    form = SearchFlightPilotForm()
    if(form.validate_on_submit()):
        idPerson = form.idPerson.data
        print("Hola mundo", idPerson)
        db = get_db()
        cursorObj = db.cursor()
        cursorObj.execute('SELECT * FROM Flight WHERE idPerson = ?',(idPerson,))
        flights = cursorObj.fetchall()
        print(flights)
    return render_template("pilot.html",form=form)

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/addFlight', methods=['GET','POST'])
def addFlight():
    form = AddFlightForm()
    if request.method == 'POST':
        depature = request.form['depature']
        arrival = request.form['arrival']
        depatureTime = request.form['depatureTime']
        arrivalTime = request.form['arrivalTime']
        plane = request.form['plane']
        capacity = request.form['capacity']
        idStatus = request.form['idStatus']
        idPerson = request.form['idPerson']
        db = get_db()
        db.execute('INSERT INTO Flight (depature, arrival, depatureTime, arrivalTime, plane, capacity, idStatus, idPerson) VALUES(?,?,?,?,?,?,?,?)',(depature, arrival, depatureTime, arrivalTime, plane, capacity, idStatus, idPerson))
        db.commit()
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