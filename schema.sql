DROP TABLE users;
DROP TABLE messages;
DROP TABLE user_groups;
DROP TABLE groups;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);
CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    max_members INTEGER,
    is_full BOOLEAN DEFAULT false,
    admin_id INTEGER REFERENCES users
);
CREATE TABLE user_groups (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    group_id INTEGER REFERENCES groups
);
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    content TEXT,
    user_id INTEGER REFERENCES users,
    group_id INTEGER REFERENCES groups,
    sent_at TIMESTAMP
);
CREATE TABLE tags (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);
CREATE TABLE group_tags (
    id SERIAL PRIMARY KEY,
    tag_id INTEGER REFERENCES tags,
    group_id INTEGER REFERENCES groups
);