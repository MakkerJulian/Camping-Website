from databasevuller import Klanten, Boekingen, db, app

def deleteklanten():
    with app.app_context():
        for i in range(len(Klanten.query.all())):
            print(f'deleted {i+1}')
            klant = Klanten.query.get(i+1)
            db.session.delete(klant)
            db.session.commit()

def deleteboekingen():
    with app.app_context():
        for i in range(len(Boekingen.query.all())):
            print(f'deleted {i+1}')
            boeking = Boekingen.query.get(i+1)
            db.session.delete(boeking)
            db.session.commit()

if __name__=='__main__':
    deleteklanten()
    deleteboekingen()