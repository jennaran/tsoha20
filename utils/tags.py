from db import db


def create_list(tags_string):
    return tags_string.split(', ')


def create_group_tag(group_id, tag_id):
    try:
        sql = "INSERT INTO group_tags (tag_id, group_id) VALUES (:tag_id, :group_id)"
        db.session.execute(sql, {"tag_id": tag_id, "group_id": group_id})
        db.session.commit()
    except:
        return False
    return True


def create_tag(tag):
    try:
        sql = "INSERT INTO tags (name) VALUES (:name) RETURNING id"
        result = db.session.execute(sql, {"name": tag})
        db.session.commit()
        tag_id: int = result.fetchone()[0]
    except:
        return -1
    return tag_id


def tag_exists(tag):
    sql = "SELECT id FROM tags WHERE name=:name"
    result = db.session.execute(sql, {"name": tag})
    return result.fetchone()


def tags_for_new_group(tags_string, group_id):
    tags = create_list(tags_string)
    for tag in tags:
        id = tag_exists(tag)
        if id:
            if not create_group_tag(group_id, id[0]):
                return False
        else:
            new_id = create_tag(tag)
            if new_id == -1:
                return False
            else:
                if not create_group_tag(group_id, new_id):
                    return False
    return True