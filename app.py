""" Para trabajar con tokens """
import os
""" from typing_extensions import Required """
""" Importar los formularios """
from forms.forms import *
""" Importar flask """
from flask import Flask, render_template, redirect, url_for, request, session
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

@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if(form.validate_on_submit()):                
        user = form.user.data
        password = form.password.data
        sql = f'SELECT * FROM Person WHERE user = "{user}"'
        db = get_db()
        cursorObj = db.cursor()
        cursorObj.execute(sql)
        users = cursorObj.fetchall()
        if len(users) > 0:
            passwordHash = users[0][2]
            if check_password_hash(passwordHash, password):
                session.clear()
                session['id'] = users[0][0]
                session['user'] = users[0][1]
                session['password'] = passwordHash
                session['idRol'] = users[0][3]
                if session['idRol'] == 1:
                    flash(f'Bienvenido(a) {user}')
                    return redirect(url_for('user'))
                elif session['idRol'] == 2:
                    flash(f'Bienvenido(a) {user}')
                    return redirect(url_for('pilot'))
                else:
                    flash(f'Bienvenido(a) {user}')
                    return redirect(url_for('admin'))
            else:
                flash('Clave incorrecta')
                return redirect(url_for('login'))
        else:
            flash('El usuario ingresado no existe')
    return render_template("login.html", form=form)

@app.route('/signUp', methods=['GET', 'POST'])
def signUp():
    form = SignUpForm()
    if request.method == 'POST':
        user = request.form['user']
        password = request.form['password']
        name = request.form['name']
        identification = request.form['identification']
        email = request.form['email']
        passwordHash = generate_password_hash(password)
        sql = 'INSERT INTO Person (user, password, idRol) VALUES (?, ?, ?)'
        sql2 = 'INSERT INTO Info (name, identification, email) VALUES (?, ?, ?)'
        db = get_db()
        result = db.execute(sql, (user, passwordHash, 1)).rowcount
        result = db.execute(sql2, (name, identification,email,)).rowcount
        db.commit()
        if result!=0:
            flash('Registro exitoso')
        else:
            flash('Woops! Hubo un error. Intenta nuevamente')
    return render_template('signUp.html', form=form)

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

@app.route('/bookFlight', methods=["GET", "POST"])
def searchBooking():
    form = BookFlightForm()
    if request.method == 'POST':
        depature = request.form['depature']
        arrival = request.form['arrival']
        depatureTime = request.form['depatureTime']
        print("Hola mundo", depature)
        sql = f'SELECT * FROM Flight WHERE depature LIKE "%{depature}%" AND arrival LIKE "%{arrival}%" AND depatureTime LIKE "%{depatureTime}%"'
        db = get_db()
        cursorObj = db.cursor()
        cursorObj.execute(sql)
        flight = cursorObj.fetchall()
        print(flight)
    return render_template("bookFlight.html",flight=flight,form=form)

@app.route('/searchFlight', methods=["GET", "POST"])
def searchFlight():
    form = SearchFlightForm()
    return render_template('searchFlight.html',form=form)

@app.route('/manageYourBooking', methods=["GET", "POST"])
def manageYourBooking():
    form = SearchFlightForm()
    if request.method == 'POST':
        idFlight = request.form['idFlight']
        print("Hola mundo", idFlight)
        sql = f'SELECT * FROM Flight WHERE id LIKE "%{idFlight}%" '
        db = get_db()
        cursorObj = db.cursor()
        cursorObj.execute(sql)
        vuelos = cursorObj.fetchall()
        print(vuelos)
    return render_template('searchFlight.html', form=form, vuelos=vuelos)

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

@app.route('/pilot', methods=["GET", "POST"])
def pilot():
    form = SearchFlightPilotForm()
    return render_template('pilot.html', form=form)

@app.route('/manageYourFlights', methods=["GET", "POST"])
def manageYourFlights():
    form = SearchFlightPilotForm()
    if request.method == 'POST':
        idPerson = request.form['idPerson']
        print("Hola mundo", idPerson)
        sql = f'SELECT * FROM Flight WHERE idPerson LIKE "%{idPerson}%"'
        db = get_db()
        cursorObj = db.cursor()
        cursorObj.execute(sql)
        flight = cursorObj.fetchall()
        print(flight)
    return render_template("pilot.html", form=form, flight=flight)

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/manageFlight')
def manageFlight():
    return render_template('manageFlight.html')

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

@app.route('/flights')
def flights():
    sql = f'SELECT * FROM Flight'
    db = get_db()
    cursorObj = db.cursor()
    cursorObj.execute(sql)
    flight = cursorObj.fetchall()
    return render_template('flights.html', flight=flight)

@app.route('/editFlight', methods=['GET','POST'])
def editFlight():
    id = request.args.get('id')
    if request.method == 'GET':
        form = AddFlightForm()
        db = get_db()
        sql = f'SELECT * FROM Flight WHERE id = {id}'
        cursorObj = db.cursor()
        cursorObj.execute(sql)
        flight = cursorObj.fetchall()[0]
        print(flight)
        return render_template('editFlight.html', form=form, flight=flight)

    if request.method == 'POST':
        id = request.form['id']
        print(id)
        depature = request.form['depature']
        arrival = request.form['arrival']
        depatureTime = request.form['depatureTime']
        arrivalTime = request.form['arrivalTime']
        plane = request.form['plane']
        capacity = request.form['capacity']
        idStatus = request.form['idStatus']
        idPerson = request.form['idPerson']
        db = get_db()
        sql = 'UPDATE Flight SET depature = ?, arrival = ?, depatureTime = ?, arrivalTime = ?, plane = ?, capacity = ?, idStatus = ?, idPerson = ? WHERE id = ?'
        result = db.execute(sql, (depature, arrival, depatureTime, arrivalTime, plane, capacity, idStatus, idPerson, id)).rowcount
        db.commit()
        if result > 0:
            flash('Actualizaste el vuelo exitosamente')
            print("okeeeeyyy")
        else:
            flash('No se pudo actualizar el vuelo')
            print("NOOOOO")            
        return redirect(url_for('flights'))

@app.route('/deleteFlight', methods=['GET','POST'])
def deleteFlight():
    id = request.args.get('id')
    print(id)
    sql = 'DELETE FROM Flight WHERE id = ?'
    db = get_db()
    db.execute(sql, (id))
    db.commit()
    db.close()
    db = get_db()
    flash('Eliminaste el vuelo exitosamente')
    return redirect(url_for('flights'))

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