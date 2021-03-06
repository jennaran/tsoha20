from db import db
from flask import session
import os
from werkzeug.security import check_password_hash, generate_password_hash


def login(username, password):
    sql = "SELECT password, id FROM users WHERE username=:username AND active=true"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    if user is None:
        return False
    else:
        if check_password_hash(user[0], password):
            session["user_id"] = user[1]
            session["csrf_token"] = os.urandom(16).hex()
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
    result = db.session.execute(sql, {"id": user_id()})
    user = result.fetchone()
    return user


def delete():
    sql1 = "DELETE FROM user_groups WHERE user_id=:id RETURNING group_id"
    result = db.session.execute(sql1, {"id": user_id()})
    group_id = result.fetchone()[0]
    print("             ",group_id)
    sql2 = "UPDATE users SET active = false WHERE id=:id"
    db.session.execute(sql2, {"id": user_id()})
    sql3 = "UPDATE groups SET is_full = false WHERE id=:id"
    db.session.execute(sql3, {"id": group_id})
    db.session.commit()
    logout()


def logout():
    del session["user_id"]


def user_id():
    return session.get("user_id", 0)


