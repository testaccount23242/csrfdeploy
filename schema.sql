INSERT INTO users (username, password, role) VALUES ('admin', 'adminpass', 'admin')
ON CONFLICT (username) DO NOTHING;

INSERT INTO users (username, password, role) VALUES ('user1', 'userpass', 'user')
ON CONFLICT (username) DO NOTHING;
