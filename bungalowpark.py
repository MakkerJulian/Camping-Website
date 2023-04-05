from flask import Flask, render_template, redirect, flash,url_for, request,session,flash
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from databasevuller import Klanten, Boekingen, db, app, Huizen
import os
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash


#Formulieren
class VotingForm(FlaskForm):
    naam = StringField('Naam')
    wachtwoord= StringField('Wachtwoord')
    email=StringField('E-mail')

class InlogFrom(FlaskForm):
    email = StringField('E-Mail')
    wachtwoord=StringField('Wachtwoord')

#login en log out
@app.route("/")
def root():
    session['logged_in'] = 0
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
        flash('Vul alle velden in om in te loggen')
        return redirect('inloggen')
    elif '@' not in email or '.' not in email:
        flash('Geen geldig mailadres opgegeven')
        return redirect('inloggen')
    
    with app.app_context():
        for x in (Klanten.query.all()):
            if x.e_mail == email:
                if check_password_hash(x.wachtwoord,wachtwoord):
                    session['logged_in'] = 1
                    session['Naam']=x.naam
                    session['Mail']=x.e_mail
                    session['id']= x.id
                    return redirect('/')
                else:
                    flash('Inloggen Mislukt, wachtwoord hoort niet bij de gegeven mail')
                    return redirect('inloggen')
        flash('Email onbekend, Maak eerst een account aan')
        return redirect('inloggen')

@app.route("/uitloggen")
def uitloggen():
    session['logged_in'] = 0
    session['Naam'] = ''
    session['Mail'] = ''
    session['id']==''
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

@app.route("/boekingen")
def boekingen():
    with app.app_context():
        if Boekingen.query.all()!=[]:
            boekingen=[]
            for x in (Boekingen.query.all()):
                if Boekingen.klanten_id== session['id']:
                    boekingen.append(x.id)
            session['boeks']=boekingen
            return render_template('boekingen.html')
        session['boeks']=['geen boekingen']
        return render_template('boekingen.html')

    


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
            session['id']=id
        else:
            highestid = Klanten.query.all()
            id=(highestid[-1].id+1)
            session['id']=id
    
    naam=form.naam.data
    wachtwoord=form.wachtwoord.data
    hashed_wachtwoord = generate_password_hash(wachtwoord)

    email=form.email.data

    if naam == '' or wachtwoord == '' or email =='':
        flash('Vul alle velden in om je aan te melden')
        return redirect('aanmelden')
    elif '@' not in email or '.' not in email:
        flash('Geen geldig mailadres opgegeven')
        return redirect('aanmelden')


    with app.app_context():
        for x in (Klanten.query.all()):
            if x.e_mail == email:
                flash('Email al bekend, probeer een andere')
                return redirect('aanmelden')

    db.session.add_all([Klanten(id, naam, hashed_wachtwoord,email)])
    db.session.commit()

    session['Naam']=naam
    session['Mail']=email
    session['logged_in'] = 1
    return redirect('/')



#Runnen
if __name__=='__main__':
    app.run(debug=True)