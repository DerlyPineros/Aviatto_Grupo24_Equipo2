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
    if 'user' in session:
        return render_template('user.html')
    else:
        return redirect(url_for('login'))

@app.route('/bookFlight')
def bookFlight():
    if 'user' in session:
        form = BookFlightForm()
        sql = "SELECT * FROM Flight"
        db = get_db()
        cursorObj = db.cursor()
        cursorObj.execute(sql)
        flight = cursorObj.fetchall()
        return render_template('bookFlight.html',form=form, flight=flight)
    else:
        return redirect(url_for('login'))

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
        if len(flight) > 0:
            flash('Tenemos estos vuelos para ti')
            print("okeeeeyyy")
        else:
            flash('No se encuentran vuelos para tu búsqueda')
            print("NOOOOO") 
    return render_template("bookFlight.html",flight=flight,form=form)

@app.route('/searchFlight', methods=["GET", "POST"])
def searchFlight():
    if 'user' in session:
        form = SearchFlightForm()
        return render_template('searchFlight.html',form=form)
    else:
        return redirect(url_for('login'))

@app.route('/manageYourBooking', methods=["GET", "POST"])
def manageYourBooking():
    if 'user' in session:
        form = SearchFlightForm()
        if request.method == 'POST':
            idFlight = request.form['idFlight']
            print("Hola mundo", idFlight)
            sql = f'SELECT Flight.depature, Flight.arrival, Flight.depatureTime, Flight.arrivalTime, Status.name FROM Flight JOIN Status ON Flight.idStatus = Status.id WHERE Flight.id LIKE "%{idFlight}%" '
            db = get_db()
            cursorObj = db.cursor()
            cursorObj.execute(sql)
            vuelos = cursorObj.fetchall()
            print(vuelos)
            if len(vuelos) > 0:
                flash('Aquí está la información de tu reserva')
                print("okeeeeyyy")
            else:
                flash('No se encuentran vuelos para tu búsqueda')
                print("NOOOOO")
        return render_template('searchFlight.html', form=form, vuelos=vuelos)
    else:
        return redirect(url_for('login'))

@app.route('/rateFlight', methods=["GET", "POST"])
def rateFlight():
    if 'user' in session:
        form = RateFlightForm()
        if request.method == 'POST':
            idFlight = request.form['idFlight']
            rate = request.form['rate']
            comment = request.form['comment']
            db = get_db()
            db.execute('INSERT INTO Rate (idFlight, rate, comment) VALUES(?,?,?)',(idFlight, rate, comment))
            db.commit()
        return render_template('rateFlight.html', form=form)
    else:
        return redirect(url_for('login'))

@app.route('/pilot', methods=["GET", "POST"])
def pilot():
    if 'user' in session and (session['idRol'] == 2):
        form = SearchFlightPilotForm()
        return render_template('pilot.html', form=form)
    else:
        return redirect(url_for('login'))

@app.route('/manageYourFlights', methods=["GET", "POST"])
def manageYourFlights():
    if 'user' in session and (session['idRol'] == 2):
        form = SearchFlightPilotForm()
        if request.method == 'POST':
            idPerson = request.form['idPerson']
            print("Hola mundo", idPerson)
            sql = f'SELECT Flight.id, Flight.depature, Flight.arrival, Flight.depatureTime, Flight.arrivalTime, Flight.plane, Flight.capacity, Status.name, Flight.idPerson FROM Flight JOIN Status ON Flight.idStatus = Status.id WHERE idPerson LIKE "%{idPerson}%"'
            db = get_db()
            cursorObj = db.cursor()
            cursorObj.execute(sql)
            flight = cursorObj.fetchall()
            print(flight)
            if len(flight) > 0:
                flash('Estos son tus vuelos asignados')
                print("okeeeeyyy")
            else:
                flash('No tienes vuelos asignados en este momento')
                print("NOOOOO") 
        return render_template("pilot.html", form=form, flight=flight)
    else:
        return redirect(url_for('login'))

@app.route('/admin')
def admin():
    if 'user' in session and (session['idRol'] == 3):
        return render_template('admin.html')
    else:
        return redirect(url_for('login'))

@app.route('/manageFlight')
def manageFlight():
    if 'user' in session and (session['idRol'] == 3):
        return render_template('manageFlight.html')
    else:
        return redirect(url_for('login'))

@app.route('/addFlight', methods=['GET','POST'])
def addFlight():
    if 'user' in session and (session['idRol'] == 3):
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
    else:
        return redirect(url_for('login'))

@app.route('/flights')
def flights():
    if 'user' in session and (session['idRol'] == 3):
        sql = f'SELECT * FROM Flight'
        db = get_db()
        cursorObj = db.cursor()
        cursorObj.execute(sql)
        flight = cursorObj.fetchall()
        return render_template('flights.html', flight=flight)
    else:
        return redirect(url_for('login'))

@app.route('/editFlight', methods=['GET','POST'])
def editFlight():
    if 'user' in session and (session['idRol'] == 3):
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
    else:
        return redirect(url_for('login'))

@app.route('/deleteFlight', methods=['GET','POST'])
def deleteFlight():
    if 'user' in session and (session['idRol'] == 3):
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
    else:
        return redirect(url_for('login'))

@app.route('/manageUser', methods=['GET'])
def manageUser():
    if 'user' in session and (session['idRol'] == 3):
        return render_template('manageUser.html')
    else:
        return redirect(url_for('login'))

@app.route('/addUser', methods=['GET','POST'])
def addUser():
    if 'user' in session and (session['idRol'] == 3):
        form = AddUserForm()
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
        return render_template('addUser.html', form=form)
    else:
        return redirect(url_for('login'))

@app.route('/users', methods=['GET','POST'])
def users():
    if 'user' in session and (session['idRol'] == 3):
        sql = f'SELECT * FROM Person INNER JOIN Info ON Person.id = Info.id WHERE Person.idRol = 1 OR Person.idRol = 3'
        db = get_db()
        cursorObj = db.cursor()
        cursorObj.execute(sql)
        user = cursorObj.fetchall()
        return render_template('users.html', user=user)
    else:
        return redirect(url_for('login'))

@app.route('/editUser', methods=['GET','POST'])
def editUser():
    if 'user' in session and (session['idRol'] == 3):
        id = request.args.get('id')
        if request.method == 'GET':
            form = AddUserForm()
            db = get_db()
            sql = f'SELECT * FROM Person INNER JOIN Info ON Person.id = Info.id WHERE Person.id = {id} AND Person.idRol = 1 OR Person.idRol = 3'
            cursorObj = db.cursor()
            cursorObj.execute(sql)
            user = cursorObj.fetchall()[0]
            print(user)
            return render_template('editUser.html', form=form, user=user)

        if request.method == 'POST':
            id = request.form['id']
            print(id)
            user = request.form['user']
            name = request.form['name']
            identification = request.form['identification']
            email = request.form['email']
            db = get_db()
            sql = 'UPDATE Person SET user = ? WHERE id = ?'
            sql1 = 'UPDATE Info SET name = ?, identification = ?, email = ? WHERE id = ?'
            result = db.execute(sql, (user, id)).rowcount
            result1 = db.execute(sql1, (name, identification, email, id)).rowcount
            db.commit()
            if result > 0:
                flash('Actualizaste el usuario exitosamente')
                print("okeeeeyyy")
            else:
                flash('No se pudo actualizar el usuario')
                print("NOOOOO")          
            return redirect(url_for('pilots'))
    else:
        return redirect(url_for('login'))

@app.route('/deleteUser', methods=['GET','POST'])
def deleteUser():
    if 'user' in session and (session['idRol'] == 3):
        id = request.args.get('id')
        print(id)
        sql = 'DELETE FROM Person WHERE id = ?'
        sql2 = 'DELETE FROM Info WHERE id = ?'
        db = get_db()
        db.execute(sql, (id))
        db.execute(sql2, (id))
        db.commit()
        db.close()
        db = get_db()
        flash('Eliminaste el usuario exitosamente')
        return redirect(url_for('users'))
    else:
        return redirect(url_for('login'))

@app.route('/managePilot', methods=['GET'])
def managePilot():
    if 'user' in session and (session['idRol'] == 3):
        return render_template('managePilot.html')
    else:
        return redirect(url_for('login'))

@app.route('/addPilot', methods=['GET','POST'])
def addPilot():
    if 'user' in session and (session['idRol'] == 3):
        form = AddPilotForm()
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
            result = db.execute(sql, (user, passwordHash, 2)).rowcount
            result = db.execute(sql2, (name, identification,email,)).rowcount
            db.commit()
            if result!=0:
                flash('Registro exitoso')
            else:
                flash('Woops! Hubo un error. Intenta nuevamente')
        return render_template('addPilot.html', form=form)
    else:
        return redirect(url_for('login'))

@app.route('/pilots', methods=['GET','POST'])
def pilots():
    if 'user' in session and (session['idRol'] == 3):
        sql = f'SELECT * FROM Person INNER JOIN Info ON Person.id = Info.id WHERE Person.idRol = 2'
        db = get_db()
        cursorObj = db.cursor()
        cursorObj.execute(sql)
        pilot = cursorObj.fetchall()
        print(pilot)
        return render_template('pilots.html', pilot=pilot)
    else:
        return redirect(url_for('login'))

@app.route('/editPilot', methods=['GET', 'POST'])
def editPilot():
    if 'user' in session and (session['idRol'] == 3):
        id = request.args.get('id')
        if request.method == 'GET':
            form = AddPilotForm()
            db = get_db()
            sql = f'SELECT * FROM Person INNER JOIN Info ON Person.id = Info.id WHERE Person.id = {id} AND Person.idRol = 2'
            cursorObj = db.cursor()
            cursorObj.execute(sql)
            pilot = cursorObj.fetchall()[0]
            print(pilot)
            return render_template('editPilot.html', form=form, pilot=pilot)

        if request.method == 'POST':
            id = request.form['id']
            print(id)
            user = request.form['user']
            name = request.form['name']
            identification = request.form['identification']
            email = request.form['email']
            db = get_db()
            sql = 'UPDATE Person SET user = ? WHERE id = ?'
            sql1 = 'UPDATE Info SET name = ?, identification = ?, email = ? WHERE id = ?'
            result = db.execute(sql, (user, id)).rowcount
            result1 = db.execute(sql1, (name, identification, email, id)).rowcount
            db.commit()
            if result > 0:
                flash('Actualizaste el piloto exitosamente')
                print("okeeeeyyy")
            else:
                flash('No se pudo actualizar el piloto')
                print("NOOOOO")          
            return redirect(url_for('pilots'))
    else:
        return redirect(url_for('login'))

@app.route('/deletePilot', methods=['GET', 'POST'])
def deletePilot():
    if 'user' in session and (session['idRol'] == 3):
        id = request.args.get('id')
        print(id)
        sql = 'DELETE FROM Person WHERE id = ?'
        sql2 = 'DELETE FROM Info WHERE id = ?'
        db = get_db()
        db.execute(sql, (id))
        db.execute(sql2, (id))
        db.commit()
        db.close()
        db = get_db()
        flash('Eliminaste el piloto exitosamente')
        return redirect(url_for('pilots'))
    else:
        return redirect(url_for('login'))