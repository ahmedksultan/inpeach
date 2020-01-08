from .models import db, User

def registerUser(email, password, firstName, lastName, grade):
    user = User(email=email, password=password, firstName=firstName, lastName=lastName, grade=grade)
    db.session.add(user)
    db.session.commit()

def authenticateUser(email, password):
    user = User.query.filter_by(email=email, password=password).first()
    if user == None:
        return False
    return True