SELECT setval(pg_get_serial_sequence('publisher', 'id'), COALESCE(MAX(id), 1)) FROM publisher;
SELECT setval(pg_get_serial_sequence('platform', 'id'), COALESCE(MAX(id), 1)) FROM platform;
SELECT setval(pg_get_serial_sequence('region', 'id'), COALESCE(MAX(id), 1)) FROM region;
SELECT setval(pg_get_serial_sequence('game', 'id'), COALESCE(MAX(id), 1)) FROM game;
SELECT setval(pg_get_serial_sequence('game_publisher', 'id'), COALESCE(MAX(id), 1)) FROM game_publisher;
SELECT setval(pg_get_serial_sequence('game_platform', 'id'), COALESCE(MAX(id), 1)) FROM game_platform;
SELECT setval(pg_get_serial_sequence('genre', 'id'), COALESCE(MAX(id), 1)) FROM genre;

CREATE TABLE inserted_records_log (
    id SERIAL PRIMARY KEY,
    session_id UUID NOT NULL,
    game_id INT NOT NULL REFERENCES game(id) ON DELETE CASCADE,
    inserted_at TIMESTAMP DEFAULT NOW()
);
