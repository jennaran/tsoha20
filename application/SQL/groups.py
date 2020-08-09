from db import db
from SQL import users


def get_list():
    sql = "SELECT G.name, G.id FROM groups G, user_groups UG, users U WHERE U.id = UG.user_id AND UG.group_id = G.id AND U.id = :id"
    result = db.session.execute(sql, {"id": users.user_id()})
    return result.fetchall()


def get_filtered_groups(filter):
    sql = "SELECT G.name, G.id, G.description FROM groups G, user_groups UG, users U WHERE U.id = UG.user_id AND UG.group_id = G.id AND G.name LIKE :name"
    result = db.session.execute(sql, {"name": "%"+filter+"%"})
    return result.fetchall()


def get_name(group_id):
    sql = "SELECT groups.name FROM groups WHERE groups.id = :id"
    result = db.session.execute(sql, {"id": group_id})
    return result.fetchall()

