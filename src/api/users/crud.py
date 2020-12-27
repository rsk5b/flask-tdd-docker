# src/api/crud.py


from src import db
from src.api.users.models import User


def get_all_users():
    users = User.query.all()
    return users


def get_user_by_id(user_id):
    user = User.query.filter_by(id=user_id).first()
    return user


def get_user_by_email(email):
    user = User.query.filter_by(email=email).first()
    return user


def add_user(username, email):
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return user


def update_user(user, username, email):
    user.username = username
    user.email = email
    db.session.commit()
    return user


def delete_user(user):
    db.session.delete(user)
    db.session.commit()
    return user
