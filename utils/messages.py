from db import db
from utils import users


def get_messages(group_id):
    sql = "SELECT U.username, M.content, M.sent_at, U.id, G.name " \
          "FROM groups G, user_groups UG, users U, messages M " \
          "WHERE U.id = UG.user_id AND UG.group_id = G.id " \
          "AND U.id = M.user_id AND M.group_id = G.id " \
          "AND G.id = :id ORDER BY M.id DESC"
    result = db.session.execute(sql, {"id": group_id})
    return result.fetchall()


def send(content, group_id):
    user_id = users.user_id()
    try:
        sql = "INSERT INTO messages (content, user_id, group_id, sent_at) " \
              "VALUES (:content, :user_id, :group_id, NOW())"
        db.session.execute(sql, {"content": content,
                                 "user_id": user_id,
                                 "group_id": group_id})
        db.session.commit()
    except():
        return False
    return True

