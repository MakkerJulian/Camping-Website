#Opdracht Bungalow Park: Julian Kloosterhuis en David Warris
#https://hanze-hbo-ict.github.io/webtech1/projecten/bungelowpark.html


from flask import Flask, render_template, redirect, flash,url_for, request, flash, session
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
import sqlite3
from flask_sqlalchemy import SQLAlchemy
import os

basedir= os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY']='shbfijsbdhsbdsdffggdghkjhgfhvj'
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///' + os.path.join(basedir, 'elections.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)
### CLASSES:
class VotingForm(FlaskForm):
    name = StringField('Wat is uw naam?')
    party = SelectField('Op welke partij wilt u stemmen?',choices = [])
    submit = SubmitField('Verzenden.')

class Voter(db.Model):
    __tablename__= 'voters'
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.Text)

    def __init__(self, name):
        self.name = name 

class Party(db.Model):
    __tablename__= 'parties'
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.Text)

    def __init__(self, name):
        self.name = name 

class Vote(db.Model):
    __tablename__='Vote'
    id=db.Column(db.Integer, primary_key= True)

    voter_id = db.Column(db.Integer, db.ForeignKey('voters.id'))
    stemmer = db.relationship('Voter', backref='Vote', uselist=False)

    party_id = db.Column(db.Integer, db.ForeignKey('parties.id'))
    partij= db.relationship('Party', backref='Vote', uselist=False)

    def __init__(self, voter_id , party_id):
        self.voter_id = voter_id
        self.party_id = party_id

    def __repr__(self):
        return f'Stemmer {self.stemmer.name} stemde op {self.partij.name} en dat is erg gay'
   
    

### ROUTES:
@app.route("/")
def root():
    return render_template('blokje.html',name='Henk')

@app.route("/person/<string:naam>")
def persoonlijke_pagina(naam):
    naam=naam.upper()
    if naam[-1]=="S":
        naam+='SY'
    else:
        naam+='RUSSY'    
    return render_template('blokje.html',name=naam)

@app.route("/accept")
def week1():
    #all_votes=query.all
    return render_template('accept.html',name=request.args.get("name"),party=request.args.get("party"))

@app.route("/laatste")
def moeder():
    return render_template('laatste.html')

@app.route("/stem")
def stem():
    form = VotingForm()
    form.party.choices = [(p.id,p.name) for p in Party.query.order_by('name')]
    return render_template('stem.html', form=form)

@app.route('/vote', methods=['get', 'post'])
def vote():
    form = VotingForm()
    form.party.choices = [(p.id,p.name) for p in Party.query.order_by('name')]

    if form.validate_on_submit() and form.name.data != "":
        flash(f"Bedankt {form.name.data} voor je stem op {form.party.data}")

        voter=Voter(form.name.data)
        db.session.add(voter)
        db.session.commit()
        party=Party(form.name.data)
        db.session.add(party)
        db.session.commit()
        voter_id=voter.id
        party_id=party.id
        vote=Voter(voter_id,party_id)
        db.session.add(vote)
        db.session.commit()
        return redirect(url_for('week1',name=form.name.data, party=form.party.data))
    return "Ongeldige stem"



if __name__=='__main__':
    app.run(debug=True)    





'''
cursor= db.cursor()
cursor.execute('select * from bedrijf')
for row in cursor:
   print(row)

db.execute("Update bedrijf set salaris = 90000 where ID = '1'; ")


SELECT *
FROM Huisje
INNER JOIN Types ON Huisje.Type = Types.ID;

'''

'''cursor=db.cursor()
huizennamen=[]
cursor.execute("SELECT Naam FROM Huizen")
for x in cursor:
    huizennamen.append(x[0])
cursor.close
'''