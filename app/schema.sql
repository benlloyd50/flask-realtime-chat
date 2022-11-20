DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS chat;
DROP TABLE IF EXISTS server;
CREATE TABLE user (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    password TEXT NOT NULL
);
CREATE TABLE chat (
    msg TEXT NOT NULL,
    user_id TEXT NOT NULL,
    time_sent REAL NOT NULL,
    server_id TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id),
    FOREIGN KEY (server_id) REFERENCES server (id)
);
CREATE TABLE server (
    id TEXT NOT NULL,
    name TEXT NOT NULL
);
-- Start with a default server until we have a way to exist without a server
INSERT INTO server VALUES('32800-07250', 'Default')