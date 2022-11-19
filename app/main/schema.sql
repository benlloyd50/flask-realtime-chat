DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS chat;
DROP TABLE IF EXISTS servers;

CREATE TABLE user (
    id TEXT PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    u_password TEXT NOT NULL
);

CREATE TABLE chat (
    msg TEXT NOT NULL,
    user_id TEXT NOT NULL,
    timestmp TIMESTAMP NOT NULL,
    server_id TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id),
    FOREIGN KEY (server_id) REFERENCES servers (id)
);

CREATE TABLE servers (
    id TEXT NOT NULL,
    serv_name TEXT NOT NULL
);