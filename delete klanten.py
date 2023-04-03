from databasevuller import Klanten, Boekingen, db, app

if __name__=='__main__':
    def deleteklanten():
        with app.app_context():
            for i in range(len(Klanten.query.all())):
                cursist_elsje = Klanten.query.get(i)
                db.session.delete(cursist_elsje)
                db.session.commit()