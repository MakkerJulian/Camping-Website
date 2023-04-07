from flask import Flask, render_template, redirect, flash,url_for, request,session,flash
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, IntegerField
from databasevuller import Klanten, Boekingen, db, app, Huizen, Types
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

class Revervatie(FlaskForm):
    weeknummer = SelectField('Welke week wilt u op vakantie?',choices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52])

four_person_bungalow = [
    "Deze knusse bungalow is perfect voor een gezin van 4 personen en biedt alle comfort voor een ontspannen vakantie.",
    "Geniet van de rust en privacy in deze gezellige bungalow voor 4 personen, compleet met een eigen terras en tuin.",
    "Verblijf in deze charmante bungalow met 4 slaapplaatsen en geniet van de prachtige omgeving en faciliteiten op het vakantiepark.",
    "Deze moderne bungalow is geschikt voor 4 personen en beschikt over alle voorzieningen om uw verblijf comfortabel te maken.",
    "Ontspan en geniet van de natuur in deze comfortabele bungalow voor 4 personen, met een gezellige woonkamer en een volledig uitgeruste keuken.",
    "Deze knusse bungalow voor 4 personen is de ideale uitvalsbasis om de omgeving te verkennen en van een ontspannen vakantie te genieten.",
    "Kom tot rust in deze sfeervolle bungalow voor 4 personen, voorzien van alle gemakken voor een aangenaam verblijf.",
    "Deze gezellige bungalow met 4 slaapplaatsen biedt een fijne plek om te ontspannen en te genieten van de natuurrijke omgeving.",
    "Verblijf in deze goed uitgeruste bungalow voor 4 personen en geniet van de vele faciliteiten op het vakantiepark.",
    "Deze knusse 4-persoons bungalow is de perfecte keuze voor een gezinsvakantie, met alle benodigde voorzieningen voor een comfortabel verblijf.",
    "Geniet van een gezellige vakantie in deze sfeervolle bungalow voor 4 personen, met een comfortabele woonkamer en een eigen terras.",
    "Deze moderne bungalow biedt plaats aan 4 personen en is van alle gemakken voorzien voor een plezierig verblijf.",
    "Kom tot rust in deze comfortabele bungalow voor 4 personen, omringd door groen en natuurlijke schoonheid.",
    "Deze gezellige bungalow voor 4 personen biedt een warme en gastvrije sfeer, perfect voor een ontspannen vakantie.",
    "Verblijf in deze knusse bungalow voor 4 personen en geniet van de rust en ruimte om u heen.",
    "Deze ruime bungalow biedt comfortabele accommodatie voor 4 personen, met een eigen terras en tuin om te ontspannen en te genieten van de natuur.",
    "Geniet van een ontspannen vakantie in deze gezellige bungalow voor 4 personen, met een volledig uitgeruste keuken en een comfortabele woonkamer.",
    "Deze moderne bungalow voor 4 personen biedt een stijlvolle en comfortabele accommodatie, ideaal voor een gezinsvakantie.",
    "Verblijf in deze knusse bungalow voor 4 personen en geniet van de vele recreatiemogelijkheden en faciliteiten op het vakantiepark.",
    "Deze gezellige bungalow biedt plaats aan 4 personen en is voorzien van alle comfort voor een ontspannen vakantie.",
    "Ontdek de natuurlijke schoonheid van de omgeving vanuit deze comfortabele bungalow voor 4 personen, met een prachtig uitzicht op de omringende natuur.",
    "Geniet van een rustig verblijf in deze knusse bungalow voor 4 personen, met een open haard en een eigen terras om te ontspannen.",
    "Deze sfeervolle bungalow voor 4 personen is een ideale keuze voor een gezinsvakantie, met tal van activiteiten en faciliteiten in de buurt.",
    "Verblijf in deze moderne bungalow voor 4 personen en geniet van de gezellige inrichting en het comfortabele interieur.",
    "Kom tot rust in deze prachtige bungalow voor 4 personen, omringd door groen en rust, ideaal voor een ontspannen vakantie.",
    "Deze ruime bungalow biedt comfortabele accommodatie voor 4 personen, met een ruime woonkamer en een eigen tuin om te ontspannen en te genieten van de omgeving.",
    "Geniet van de natuurlijke omgeving en rust in deze gezellige bungalow voor 4 personen, met een terras en een barbecue om te genieten van de buitenlucht.",
    "Deze comfortabele bungalow voor 4 personen biedt een aangenaam verblijf, met een goed uitgeruste keuken en een gezellige woonkamer.",
    "Verblijf in deze knusse bungalow voor 4 personen en geniet van de privacy en de rustige omgeving voor een ontspannen vakantie.",
    "Deze gezellige bungalow voor 4 personen is een ideale uitvalsbasis om de omgeving te verkennen en van de natuur te genieten, met tal van wandel- en fietsroutes in de buurt."
]

six_person_bungalow = [
    "Geniet met het hele gezin van een comfortabel verblijf in deze ruime bungalow voor 6 personen, voorzien van moderne faciliteiten en een gezellige sfeer.",
    "Deze prachtige bungalow voor 6 personen biedt een idyllische vakantieplek, omringd door de natuur en met voldoende ruimte voor ontspanning en recreatie.",
    "Kom tot rust in deze luxe bungalow voor 6 personen, met een privéterras, een sauna en alle gemakken die nodig zijn voor een ontspannen verblijf.",
    "Deze gezellige bungalow voor 6 personen is perfect voor een gezinsvakantie, met een goed uitgeruste keuken, een ruime woonkamer en een eigen tuin om van te genieten.",
    "Verblijf in deze comfortabele bungalow voor 6 personen en geniet van de rustige omgeving, de natuurlijke schoonheid en de vele recreatiemogelijkheden in de buurt.",
    "Ontdek de prachtige omgeving vanuit deze charmante bungalow voor 6 personen, met een knusse inrichting en een terras om te genieten van de buitenlucht.",
    "Deze moderne bungalow voor 6 personen biedt een stijlvol verblijf met alle voorzieningen die u nodig heeft, inclusief een goed uitgeruste keuken en een ruime woonkamer.",
    "Geniet van een ontspannen vakantie in deze ruime bungalow voor 6 personen, met een privéterras, een barbecue en tal van activiteiten in de omgeving.",
    "Deze sfeervolle bungalow voor 6 personen is een ideale keuze voor een gezinsvakantie, met een gezellige inrichting, een open haard en een privéterras.",
    "Verblijf in deze rustige bungalow voor 6 personen, omringd door de natuur en met voldoende ruimte om te ontspannen, zowel binnen als buiten.",
    "Deze gezellige bungalow voor 6 personen biedt een knusse sfeer en alle voorzieningen die nodig zijn voor een aangenaam verblijf, inclusief een goed uitgeruste keuken en een eigen tuin.",
    "Ontspan in deze comfortabele bungalow voor 6 personen, met moderne faciliteiten en een gezellige inrichting om van te genieten na een dag vol avontuurlijke activiteiten.",
    "Deze ruime bungalow voor 6 personen is perfect voor een gezinsvakantie, met voldoende ruimte om te ontspannen, een privéterras en tal van recreatiemogelijkheden in de omgeving.",
    "Geniet van de natuurlijke omgeving vanuit deze prachtige bungalow voor 6 personen, met een rustige ligging, een privétuin en een terras om van te genieten.",
    "Deze ruime bungalow voor 6 personen is perfect voor een ontspannen vakantie, met een gezellige inrichting, een privéterras en veel recreatiemogelijkheden.",
    "Geniet van een gezellig verblijf in deze knusse bungalow voor 6 personen, met een open haard, een goed uitgeruste keuken en een eigen tuin om te ontspannen.",
    "Verblijf in deze comfortabele bungalow voor 6 personen en geniet van de rustige omgeving, het privéterras en de vele activiteiten in de buurt.",
    "Deze moderne bungalow voor 6 personen biedt een luxe vakantie-ervaring, met een sauna, een privétuin en alle voorzieningen die u nodig heeft.",
    "Kom tot rust in deze sfeervolle bungalow voor 6 personen, met een gezellige inrichting, een terras om te ontspannen en de natuurlijke schoonheid in de omgeving.",
    "Ontdek de prachtige omgeving vanuit deze goed gelegen bungalow voor 6 personen, met moderne faciliteiten, een ruime woonkamer en een privéterras.",
    "Deze gezinsvriendelijke bungalow voor 6 personen biedt een comfortabel verblijf, met een speelkamer, een privéterras en veel ruimte om te ontspannen.",
    "Geniet van de natuurlijke omgeving in deze rustige bungalow voor 6 personen, met een privétuin, een barbecue en een gezellige inrichting.",
    "Deze charmante bungalow voor 6 personen biedt een idyllische vakantieplek, omringd door groen, met een terras om te genieten van de buitenlucht.",
    "Verblijf in deze gezellige bungalow voor 6 personen en geniet van de knusse inrichting, een goed uitgeruste keuken en een eigen tuin om te ontspannen.",
    "Deze ruime bungalow voor 6 personen is ideaal voor een gezinsvakantie, met een privéterras, een speelveld en tal van recreatiemogelijkheden in de buurt.",
    "Geniet van een comfortabel verblijf in deze moderne bungalow voor 6 personen, met een sauna, een privétuin en alle voorzieningen die u nodig heeft.",
    "Deze gezellige bungalow voor 6 personen biedt een knusse vakantie-ervaring, met een open haard, een privéterras en veel ruimte om te ontspannen.",
    "Ontspan in deze comfortabele bungalow voor 6 personen, met moderne faciliteiten, een gezellige inrichting en een privétuin om van te genieten.",
    "Deze prachtige bungalow voor 6 personen biedt een luxe verblijf, met een privéterras, een barbecue en tal van recreatiemogelijkheden in de omgeving.",
    "Deze gezinsvriendelijke bungalow voor 6 personen biedt een comfortabel verblijf, met een speelkamer, een privéterras en veel ruimte om te ontspannen.",
]

eight_person_bungalow = [
    "Deze ruime bungalow voor 8 personen biedt alle comfort voor een ontspannen vakantie, met een grote woonkamer, een open haard en een privéterras.",
    "Geniet van een gezellig verblijf in deze knusse bungalow voor 8 personen, met een goed uitgeruste keuken, een ruime eethoek en een eigen tuin om te ontspannen.",
    "Verblijf in deze comfortabele bungalow voor 8 personen en geniet van de rustige omgeving, het privéterras en de vele activiteiten in de buurt.",
    "Deze moderne bungalow voor 8 personen biedt een luxueuze vakantie-ervaring, met een sauna, een privétuin en alle voorzieningen die u nodig heeft.",
    "Kom tot rust in deze sfeervolle bungalow voor 8 personen, met een gezellige inrichting, een terras om te ontspannen en de natuurlijke schoonheid in de omgeving.",
    "Ontdek de prachtige omgeving vanuit deze goed gelegen bungalow voor 8 personen, met moderne faciliteiten, een ruime woonkamer en een privéterras.",
    "Deze gezinsvriendelijke bungalow voor 8 personen biedt een comfortabel verblijf, met een speelkamer, een privéterras en veel ruimte om te ontspannen.",
    "Geniet van de natuurlijke omgeving in deze rustige bungalow voor 8 personen, met een privétuin, een barbecue en een gezellige inrichting.",
    "Deze charmante bungalow voor 8 personen biedt een idyllische vakantieplek, omringd door groen, met een terras om te genieten van de buitenlucht.",
    "Verblijf in deze gezellige bungalow voor 8 personen en geniet van de knusse inrichting, een goed uitgeruste keuken en een eigen tuin om te ontspannen.",
    "Deze ruime bungalow voor 8 personen is ideaal voor een gezinsvakantie, met een privéterras, een speelveld en tal van recreatiemogelijkheden in de buurt.",
    "Geniet van een comfortabel verblijf in deze moderne bungalow voor 8 personen, met een sauna, een privétuin en alle voorzieningen die u nodig heeft.",
    "Deze gezellige bungalow voor 8 personen biedt een knusse vakantie-ervaring, met een open haard, een privéterras en veel ruimte om te ontspannen.",
    "Ontspan in deze comfortabele bungalow voor 8 personen, met moderne faciliteiten, een gezellige inrichting en een privétuin om van te genieten.",
    "Deze prachtige bungalow voor 8 personen biedt een luxe verblijf, met een privéterras, een barbecue en tal van recreatiemogelijkheden in de omgeving.",
    "Deze ruime bungalow voor 8 personen biedt volop comfort voor een ontspannen vakantie, met een grote woonkamer, een open haard en een privéterras.",
    "Geniet van een gezellig verblijf in deze knusse bungalow voor 8 personen, met een goed uitgeruste keuken, een ruime eethoek en een eigen tuin om te ontspannen.",
    "Verblijf in deze comfortabele bungalow voor 8 personen en geniet van de rustige omgeving, het privéterras en de vele activiteiten in de buurt.",
    "Deze moderne bungalow voor 8 personen biedt een luxueuze vakantie-ervaring, met een sauna, een privétuin en alle voorzieningen die je nodig hebt.",
    "Kom tot rust in deze sfeervolle bungalow voor 8 personen, met een gezellige inrichting, een terras om te ontspannen en de natuurlijke schoonheid in de omgeving.",
    "Ontdek de prachtige omgeving vanuit deze goed gelegen bungalow voor 8 personen, met moderne faciliteiten, een ruime woonkamer en een privéterras.",
    "Deze gezinsvriendelijke bungalow voor 8 personen biedt een comfortabel verblijf, met een speelkamer, een privéterras en veel ruimte om te ontspannen.",
    "Geniet van de natuurlijke omgeving in deze rustige bungalow voor 8 personen, met een privétuin, een barbecue en een gezellige inrichting.",
    "Deze charmante bungalow voor 8 personen biedt een idyllische vakantieplek, omringd door groen, met een terras om te genieten van de buitenlucht.",
    "Verblijf in deze gezellige bungalow voor 8 personen en geniet van de knusse inrichting, een goed uitgeruste keuken en een eigen tuin om te ontspannen.",
    "Deze ruime bungalow voor 8 personen is ideaal voor een gezinsvakantie, met een privéterras, een speelveld en tal van recreatiemogelijkheden in de buurt.",
    "Geniet van een comfortabel verblijf in deze moderne bungalow voor 8 personen, met een sauna, een privétuin en alle voorzieningen die je nodig hebt.",
    "Deze gezellige bungalow voor 8 personen biedt een knusse vakantie-ervaring, met een open haard, een privéterras en veel ruimte om te ontspannen.",
    "Ontspan in deze comfortabele bungalow voor 8 personen, met moderne faciliteiten, een gezellige inrichting en een privétuin om van te genieten.",
    "Deze prachtige bungalow voor 8 personen biedt een luxe verblijf, met een privéterras, een barbecue en tal van recreatiemogelijkheden in de omgeving.",
]




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
    session['id']=''
    session['namen']=''
    session['types']= ''
    session['boeks']=''
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

@app.route('/aanpassen')
def aanpassen():
    form= Revervatie()
    huid= int(request.args.get('buttonValue'))
    with app.app_context():
        if Boekingen.query.all()!=[]:
            huisnaam=''
            for x in (Boekingen.query.join(Huizen,Boekingen.Bungalow_id==Huizen.id).add_columns(Boekingen.id, Huizen.naam,).all()):
                if x.id == huid:
                    huisnaam= x.naam
                    huisnaam=huisnaam.split()[1]
    return render_template('aanpassen.html',form=form, huisnaam=huisnaam)

@app.route('/annuleren')
def annuleren():
    anuid= int(request.args.get('buttonValue'))
    with app.app_context():
        for i in Boekingen.query.all():
            if i.id == anuid:
                db.session.delete(i)
            db.session.commit()
        return redirect('boekingen')

@app.route("/boekingen")
def boekingen():
    with app.app_context():
        if Boekingen.query.all()!=[]:
            boekingen=[]
            for x in (Boekingen.query.join(Huizen,Boekingen.Bungalow_id==Huizen.id).add_columns(Boekingen.id, 
                                                                                                Boekingen.klanten_id, 
                                                                                                Boekingen.weeknummer, 
                                                                                                Huizen.naam,
                                                                                                Huizen.type
                                                                                                ).all()):
                if x.klanten_id == session['id']:
                    boekingen.append((x.id, x.weeknummer, x.naam,x.type))
            session['boeks']=boekingen
        types=[]
        for x in (Types.query.all()):
                types.append((x.id,x.personen,x.weekprijs))
        session['types']=types

        return render_template('boekingen.html')


@app.route('/huisinfo' ,  methods=['POST','GET'])
def huisinfo():
    form= Revervatie()
    huisnaam = request.args.get('buttonValue')
    session['huisnaam']= huisnaam
    for x in (Huizen.query.join(Types, Huizen.type == Types.id).add_columns(Huizen.id, Huizen.naam, Types.personen )):
        if huisnaam in x.naam:
            if x.personen == 4:
                beschrijving= four_person_bungalow[x.id-1]
            elif x.personen == 6:
                beschrijving= six_person_bungalow[x.id-11]
            elif x.personen == 8:
                beschrijving = eight_person_bungalow[x.id-21]
    # Do something with the button value, such as displaying it on the page
    return render_template('huisinfo.html', huisnaam=huisnaam, form=form, beschrijving=beschrijving)

@app.route('/reserveren', methods=['POST','GET'])
def reserveren():
    form = Revervatie()
    with app.app_context():
        if Boekingen.query.all()==[]:
            id=1
        else:
            highestid = Boekingen.query.all()
            id=(highestid[-1].id+1)
    
    k_id=session['id']

    huisnaam=session['huisnaam']
    with app.app_context():
        for x in (Huizen.query.all()):
            if huisnaam in x.naam:
                h_id= x.id
    
    wnr=form.weeknummer.data

    db.session.add_all([Boekingen(id, k_id, h_id, wnr)])
    db.session.commit()
    return redirect('boekingen')


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