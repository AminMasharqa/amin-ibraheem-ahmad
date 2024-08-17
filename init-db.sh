#!/bin/bash
set -e

# Create tables in the PostgreSQL database
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL

    -- Create the genre table
    CREATE TABLE IF NOT EXISTS genre (
        genre_id SERIAL PRIMARY KEY,
        genre_name VARCHAR(100) NOT NULL
    );

    -- Create the artists table
    CREATE TABLE IF NOT EXISTS artists (
        artist_id SERIAL PRIMARY KEY,
        genre_id INTEGER REFERENCES genre(genre_id),
        artist_name VARCHAR(100) NOT NULL,
        country VARCHAR(100) NOT NULL,
        gender VARCHAR(10)
    );

    -- Create the songs table
    CREATE TABLE IF NOT EXISTS songs (
        song_id SERIAL PRIMARY KEY,
        artist_id INTEGER REFERENCES artists(artist_id),
        genre_id INTEGER REFERENCES genre(genre_id),
        song_name VARCHAR(200) NOT NULL,
        language VARCHAR(50),
        release_date DATE,
        album_img VARCHAR(255),
        song_link VARCHAR(255) NOT NULL,
        streams BIGINT,
        duration INTEGER
    );

    -- Create the ranking table
    CREATE TABLE IF NOT EXISTS ranking (
        ranking_id SERIAL PRIMARY KEY,
        song_id INTEGER REFERENCES songs(song_id),
        chart_name VARCHAR(100),
        chart_link VARCHAR(255),
        current_rank INTEGER,
        previous_rank INTEGER,
        rank_date DATE
    );

EOSQL
