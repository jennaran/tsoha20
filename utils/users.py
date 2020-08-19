from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash


def login(username, password):
    sql = "SELECT password, id FROM users WHERE username=:username"
    result = db.session.execute(sql, {'username': username})
    user = result.fetchone()
    if user is None:
        return False
    else:
        if check_password_hash(user[0], password):
            session["user_id"] = user[1]
            return True
        else:
            return False


def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username,password) VALUES (:username,:password)"
        db.session.execute(sql, {"username": username, "password": hash_value})
        db.session.commit()
    except:
        return False
    return login(username, password)


def get_user():
    sql = "SELECT username FROM users WHERE id=:id"
    result = db.session.execute(sql, {'id': user_id()})
    user = result.fetchone()
    return user


def delete():
    id = user_id()
    print("id on", id)
    try:
        sql = "DELETE FROM user_groups WHERE user_id=:id"
        db.session.execute(sql, {'id': id})
        db.session.commit()
        sql = "DELETE FROM users WHERE id=:id"
        db.session.execute(sql, {'id': id})
        db.session.commit()
        logout()
    except:
        return False
    return True


def logout():
    del session["user_id"]


def user_id():
    return session.get("user_id", 0)


