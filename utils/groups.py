from db import db
from utils import users, tags


def get_list():
    sql = "SELECT DISTINCT G.name, G.id " \
          "FROM groups G, user_groups UG, users U " \
          "WHERE U.id = UG.user_id AND UG.group_id = G.id AND U.id = :id"
    result = db.session.execute(sql, {"id": users.user_id()})
    return result.fetchall()


def get_filtered_groups(filter):
    sql = "SELECT DISTINCT G.name, G.id, G.description, G.max_members " \
          "FROM groups G, user_groups UG, users U, group_tags GT, tags T " \
          "WHERE U.id = UG.user_id AND UG.group_id = G.id " \
          "AND G.id = GT.group_id AND GT.tag_id = T.id " \
          "AND G.id NOT IN (" \
                "SELECT G.id " \
                "FROM groups G, user_groups UG, users U " \
                "WHERE U.id = UG.user_id AND UG.group_id = G.id AND U.id = :id) " \
          "AND (LOWER(G.name) LIKE :name OR LOWER(T.name) LIKE :name) AND G.is_full = false"
    result = db.session.execute(sql, {"id": users.user_id(), "name": "%"+filter+"%"})
    return result.fetchall()


def get_info(group_id):
    sql = "SELECT DISTINCT G.name, G.max_members, U.username, G.description, G.id " \
          "FROM groups G, user_groups UG, users U " \
          "WHERE G.id = :group_id AND U.id = G.admin_id"
    result = db.session.execute(sql, {"group_id": group_id})
    return result.fetchone()


def get_name(group_id):
    sql = "SELECT groups.name FROM groups WHERE groups.id = :id"
    result = db.session.execute(sql, {"id": group_id})
    return result.fetchall()


def get_max_members(group_id):
    sql = "SELECT DISTINCT max_members from groups WHERE id = :group_id"
    result = db.session.execute(sql, {"group_id": group_id})
    return result.fetchone()


def get_member_count(group_id):
    sql = "SELECT COUNT(*) FROM user_groups WHERE group_id = :group_id"
    result = db.session.execute(sql, {"group_id": group_id})
    return result.fetchone()


def get_members(group_id):
    sql = "SELECT DISTINCT U.username " \
          "FROM groups G, user_groups UG, users U " \
          "WHERE U.id = UG.user_id AND UG.group_id = G.id AND G.id = :group_id " \
          "ORDER BY U.username"
    result = db.session.execute(sql, {"group_id": group_id})
    return result.fetchall()


def is_a_member(group_id):
    sql = "SELECT id FROM user_groups WHERE group_id=:group_id AND user_id=:user_id"
    result = db.session.execute(sql, {"group_id": group_id, "user_id": users.user_id()})
    return result.fetchall()


def is_full(group_id):
    print("full")
    sql = "SELECT is_full FROM groups WHERE id=:group_id"
    result = db.session.execute(sql, {"group_id": group_id})
    print(result.fetchone())
    return result.fetchone()


def set_full(group_id):
    try:
        sql = "UPDATE groups SET is_full = true WHERE id = :group_id"
        db.session.execute(sql, {"group_id": group_id})
        db.session.commit()
    except:
        return False
    return True


def join_a_group(group_id):
    if is_full(group_id):
        return False
    else:
       print("ryhmässä tilaa")
       try:
           sql = "INSERT INTO user_groups (user_id, group_id) VALUES (:user_id, :group_id)"
           db.session.execute(sql, {"user_id": users.user_id(), "group_id": group_id})
           member_count = get_member_count(group_id)
           max_members = get_max_members(group_id)
           if member_count == max_members:
               set_full(group_id)
           db.session.commit()
       except:
           return False
       return True



def leave_a_group(group_id):
    try:
        sql = "DELETE FROM user_groups WHERE user_id = :user_id AND group_id = :group_id"
        db.session.execute(sql, {"user_id": users.user_id(), "group_id": group_id})
        sql2 = "UPDATE groups SET is_full = false WHERE id = :group_id"
        db.session.execute(sql2, {"group_id": group_id})
        db.session.commit()
    except:
        return False
    return True


def new_group(name, info, tags_string, limit):
    try:
        sql = "INSERT INTO groups (name, description, max_members, admin_id) " \
              "VALUES (:name, :description, :max_members, :admin_id) RETURNING id"
        result = db.session.execute(sql, {
            "name": name,
            "description": info,
            "max_members": limit,
            "admin_id": users.user_id()
        })
        group_id = result.fetchone()[0]
        tags.tags_for_new_group(tags_string, group_id)
        join_a_group(group_id)
        db.session.commit()
    except:
        return None
    return group_id
