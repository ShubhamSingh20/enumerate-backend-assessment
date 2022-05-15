from app import app, db

if __name__ == '__main__':
    from app.models import *
    from app.controllers import *

    db.create_all()
    db.session.commit()

    app.run()