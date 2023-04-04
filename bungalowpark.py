from flask import Flask, render_template, redirect, flash,url_for, request,session
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from databasevuller import Klanten, Boekingen, db, app
import os
from flask_sqlalchemy import SQLAlchemy


#Formulieren
class VotingForm(FlaskForm):
    naam = StringField('Naam')
    wachtwoord= StringField('Wachtwoord')
    email=StringField('E-mail')
    submit = SubmitField('Aanmelden')

class InlogFrom(FlaskForm):
    email = StringField('E-Mail')
    wachtwoord=StringField('Wachtwoord')
    submit = SubmitField('Inloggen')


#login en log out

@app.route("/")
def root():
    session['logged_in'] = 0
    return render_template('bungalowpark.html')

@app.route("/inloggen")
def aanmelden():
    form = InlogFrom()
    print(form)
    return render_template('inloggen.html', form=form)

@app.route("/uitloggen")
def uitloggen():
    session['logged_in'] = 0
    return render_template('bungalowpark.html', gebruikersnaam = '')

#aanmelden 
@app.route("/aanmelden")
def inloggen():
    form = VotingForm()
    return render_template('aanmelden.html', form=form)

#Huizen:
@app.route("/4p")
def vierp():
    return render_template('4huis.html')

@app.route("/6p")
def zesp():
    return render_template('6huis.html')

@app.route("/8p")
def achtp():
    return render_template('8huis.html')


@app.route("/contact")
def contact():
    return render_template('contact.html')



#Aanmelden en account aanmaken
@app.route("/aangemeld" , methods=['POST','GET'])
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

    with app.app_context():
        for x in (Klanten.query.all()):
            if x.e_mail == email:
                return 'Email al bekend, probeer opnieuw'
            

    db.session.add_all([Klanten(id, naam, wachtwoord,email)])
    db.session.commit()

    session['logged_in'] = 1
    return render_template('bungalowpark.html', gebruikersnaam=naam)


#Runnen
if __name__=='__main__':
    app.run(debug=True)

