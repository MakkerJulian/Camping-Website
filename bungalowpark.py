from flask import Flask, render_template, redirect, flash,url_for, request,session
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from databasevuller import Klanten, Boekingen, db, app, Huizen
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
    return render_template('bungalowpark.html')

@app.route("/inloggen")
def aanmelden():
    form = InlogFrom()
    return render_template('inloggen.html', form=form)

@app.route("/ingelogd", methods=['POST','GET'])
def ingelogd():
    form = InlogFrom()
    email=form.email.data
    wachtwoord = form.wachtwoord.data

    if email == '' or wachtwoord=='':
        return 'Vul alle velden in om in te loggen'
    elif '@' not in email or '.' not in email:
        return 'Geen geldig mailadres opgegeven'
    
    with app.app_context():
        for x in (Klanten.query.all()):
            if x.e_mail == email:
                if x.wachtwoord==wachtwoord:
                    session['logged_in'] = 1
                    session['Naam']=x.naam
                    session['Mail']=x.e_mail
                    return redirect('/')
                
                else:
                    return 'Inloggen Mislukt, wachtwoord hoort niet bij de gegeven mail'
        return 'Email onbekend, Maak eerst een account aan'

@app.route("/uitloggen")
def uitloggen():
    session['logged_in'] = 0
    session['Naam'] = ''
    session['Mail'] = ''
    return redirect('/')

@app.route('/huis')
def huis():
    return render_template('huis.html')

#Huizen:
@app.route("/4p")
def vierp():
    session['ap'] = '4'
    huizennamen=[]
    with app.app_context():
        for x in (Huizen.query.all()):
            if x.type ==1:
                huizennamen.append(x.naam)
    session['namen']=huizennamen
    return redirect('huis')

@app.route("/6p")
def zesp():
    session['ap'] = '6'
    huizennamen=[]
    with app.app_context():
        for x in (Huizen.query.all()):
            if x.type ==2:
                huizennamen.append(x.naam)
    session['namen']=huizennamen
    return redirect('huis')

@app.route("/8p")
def achtp():
    huizennamen=[]
    with app.app_context():
        for x in (Huizen.query.all()):
            if x.type ==3:
                huizennamen.append(x.naam)
    session['namen']=huizennamen
    session['ap'] = '8'
    return redirect('huis')

#contact
@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route('/boeken')
def boeken():
    huisnaam = request.args.get('buttonValue')
    # Do something with the button value, such as displaying it on the page
    return render_template('boeken.html', huisnaam=huisnaam)


#Aanmelden en account aanmaken
@app.route("/aanmelden")
def inloggen():
    form = VotingForm()
    return render_template('aanmelden.html', form=form)

@app.route("/aangemeld" , methods=['POST','GET'])
def aangemeld():
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

    session['Naam']=naam
    session['Mail']=email
    session['logged_in'] = 1
        
    return redirect('/')



#Runnen
if __name__=='__main__':
    app.run(debug=True)