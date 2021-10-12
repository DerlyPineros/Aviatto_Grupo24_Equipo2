""" Para poder trabajar con tokens """
import os
""" Importar los formularios """
from forms.forms import *
""" Importar flask """
from flask import Flask, render_template
from forms.forms import BookFlightForm

app = Flask(__name__)
""" metodo para usar el token """
app.secret_key = os.urandom(24)

""" Ruta inicial """
@app.route('/')
def start():
    return render_template('index.html')

""" Ruta vista principal usuario (Tengo el metodo get y post para el form)"""
@app.route("/user/", methods=['GET','POST'])
def user():
    return render_template('user.html')

@app.route("/user/bookFlight", methods=["GET", "POST"])
def bookFlight():
    form = BookFlightForm()
    return render_template('bookFlight.html', form=form)

@app.route("/user/searchFlight", methods=["GET", "POST"])
def searchFlight():
    form = SearchFlightForm()
    return render_template('searchFlight.html', form=form)

@app.route("/user/rateFlight", methods=["GET", "POST"])
def rateFlight():
    form = RateFlightForm()
    return render_template('rateFlight.html', form=form)

@app.route("/pilot", methods=["GET", "POST"])
def pilot():
    form = SearchFlightPilotForm()
    return render_template("pilot.html",form=form)