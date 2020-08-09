CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL ,
    password TEXT NOT NULL
);
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    content TEXT,
    user_id INTEGER REFERENCES users,
    group_id INTEGER REFERENCES groups,
    sent_at TIMESTAMP
);
CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL
);
CREATE TABLE user_groups (
    user_id INTEGER REFERENCES users,
    group_id INTEGER REFERENCES groups
);