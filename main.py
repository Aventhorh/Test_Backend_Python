from models.User import db
from services.UserService import app

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=4000)
