CREATE INDEX idx_user_email ON users (email);
EXPLAIN ANALYZE SELECT * from users
DROP INDEX IF EXISTS idx_user_email;