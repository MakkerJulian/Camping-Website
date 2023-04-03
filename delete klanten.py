from databasevuller import Klanten, Boekingen, db, app
if __name__=='__main__':
    def deleteklanten():
        with app.app_context():
            for i in range(len(Klanten.query.all())):
                print(f'deleted {i+1}')
                cursist_elsje = Klanten.query.get(i+1)
                db.session.delete(cursist_elsje)
                db.session.commit()

