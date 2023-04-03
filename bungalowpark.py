from flask import Flask, render_template, redirect, flash,url_for, request,session
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from databasevuller import Klanten, Boekingen, db, app
import os
from flask_sqlalchemy import SQLAlchemy

class VotingForm(FlaskForm):
    naam = StringField('Wat is uw naam?')
    wachtwoord= StringField('Voer hier je wachtwoord in')
    email=StringField('Voer hier je e-mail in')
    submit = SubmitField('Inloggen')



class inloggen(FlaskForm):
    name = StringField('E-mail')
    party = SelectField('wachtwoord')
    submit = SubmitField('Verzenden.')



@app.route("/")
def root():
    session['logged_in'] = 0
    return render_template('bungalowpark.html')

@app.route("/inloggen")
def inloggen():
    form = VotingForm()
    return render_template('inloggen.html', form=form)

@app.route("/aanmelden")
def aanmelden():
    return render_template('aanmelden.html')

@app.route("/huizen")
def huizen():
    return render_template('huizen.html')

@app.route("/contact")
def contact():
    return render_template('contact.html')


@app.route("/ingelogd" , methods=['POST','GET'])
def ingelogd():
    form=VotingForm()
    with app.app_context():
        if Klanten.query.all()==[]:
            id=1
        else:
            highestid = Klanten.query.all()
            id=(highestid[-1].id+1)

    naam=form.naam.data
    wachtwoord=form.wachtwoord.data
    email=form.email.data
    db.session.add_all([Klanten(id, naam, wachtwoord,email)])
    db.session.commit()

    session['logged_in'] = 1
    return render_template('bungalowpark.html', gebruikersnaam=naam)

if __name__=='__main__':
    app.run(debug=True)

