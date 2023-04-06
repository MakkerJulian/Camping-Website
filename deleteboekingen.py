from databasevuller import Klanten, Boekingen, db, app

def deleteboekingen():
    with app.app_context():
        for i in range(len(Boekingen.query.all())):
            print(f'deleted {i+1}')
            cursist_elsje = Boekingen.query.get(i+1)
            db.session.delete(cursist_elsje)
            db.session.commit()

if __name__=='__main__':
    deleteboekingen()