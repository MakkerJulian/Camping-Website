import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

namen = ['De Zonnewijzer', 'De Roos', 'De Hoop', 'De Lelie', 'De Linden', 'De Vlinder',
                      'De Korenmolen', 'De Erik', 'De Appelboom', 'De Wilg', 'De Berk', 'De Beuk', 'De Esdoorn', 
                      'De Herberg', 'De Wielewaal', 'De Leeuwerik', 'De Kievit', 'De Nachtegaal', 'De Merel', 'De Zwaluw', 
                      'De Duif', 'De Koolmees', 'De Putter', 'De Kruisstraat', 'De Klaproos', 'De Tulp', 'De Hyacint', 'De Narcis', 
                      'De Ridderspoor', 'De Lavendel']


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY']='shbfijsbdhsbdsdffggdghkjhgfhvj'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'Bungalow.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db=SQLAlchemy(app)


class Huizen(db.Model):
    __tablename__ = 'Huizen'
    id = db.Column(db.Integer,primary_key=True)
    naam = db.Column(db.Text)
    type = db.Column(db.Integer)

    def __init__(self,id,naam,type):
        self.id=id
        self.naam = naam
        self.type = type

class Klanten(db.Model):
    __tablename__ = 'Klanten'
    id = db.Column(db.Integer,primary_key=True)
    naam = db.Column(db.Text)
    wachtwoord = db.Column(db.Text)
    e_mail = db.Column(db.VARCHAR)

    def __init__(self,id,naam,wachtwoord,e_mail):
        self.id=id
        self.naam = naam
        self.wachtwoord = wachtwoord
        self.e_mail = e_mail

    def __str__(self):
        return f'{self.id}'
    
class Types(db.Model):
    __tablename__ = 'Types'
    id = db.Column(db.Integer,primary_key=True)
    personen = db.Column(db.Integer)
    weekprijs = db.Column(db.Integer)

    def __init__(self,id,personen,weekprijs):
        self.id=id
        self.personen = personen
        self.weekprijs = weekprijs

#de lastigste
class Boekingen(db.Model):
    __tablename__='Boekingen'
    id=db.Column(db.Integer,primary_key=True)
    klanten_id= db.Column(db.Integer, db.ForeignKey('Klanten.id'))
    Klanten = db.relationship('Klanten', backref='Boekingen', uselist=False)
    Bungalow_id= db.Column(db.Integer, db.ForeignKey('Huizen.id'))
    stemmer = db.relationship('Huizen', backref='Boekingen', uselist=False)
    weeknummer= db.Column(db.Integer)
    lengte= db.Column(db.Integer)
    
    def __init__(self, id, klanten_id , bungalow_id, weeknummer,lengte):
        self.id=id 
        self.klanten_id = klanten_id
        self.Bungalow_id = bungalow_id 
        self.weeknummer = weeknummer
        self.lengte= lengte
#Runnen
if __name__=='__main__':
    with app.app_context():
        db.create_all()
        for i in range(len(namen)):
            db.session.add_all([Huizen(i+1, namen[i], i//10+1)])
        db.session.add_all([Types(1,4,200),Types(2,6,300),Types(3,8,600)])
        db.session.commit()