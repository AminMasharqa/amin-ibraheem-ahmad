#!/bin/bash
set -e

# Create tables in the PostgreSQL database
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    -- Create platforms table
    CREATE TABLE IF NOT EXISTS platforms (
        platform_id SERIAL PRIMARY KEY,
        name VARCHAR(255) UNIQUE NOT NULL
    );

    -- Create genres table
    CREATE TABLE IF NOT EXISTS genres (
        genre_id SERIAL PRIMARY KEY,
        name VARCHAR(255) UNIQUE NOT NULL
    );

    -- Create languages table
    CREATE TABLE IF NOT EXISTS languages (
        language_id SERIAL PRIMARY KEY,
        name VARCHAR(255) UNIQUE NOT NULL
    );

    -- Create artists table
    CREATE TABLE IF NOT EXISTS artists (
        artist_id SERIAL PRIMARY KEY,
        name VARCHAR(255) UNIQUE NOT NULL,
        platform_id INT REFERENCES platforms(platform_id) ON DELETE CASCADE
    );

    -- Create songs table
    CREATE TABLE IF NOT EXISTS songs (
        song_id SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        artist_id INT REFERENCES artists(artist_id) ON DELETE CASCADE,
        album VARCHAR(255),
        duration INTERVAL,
        spotify_url TEXT,
        genre_id INT REFERENCES genres(genre_id) ON DELETE SET NULL,
        language_id INT REFERENCES languages(language_id) ON DELETE SET NULL,
        platform_id INT REFERENCES platforms(platform_id) ON DELETE SET NULL
    );

    -- Create charts table
    CREATE TABLE IF NOT EXISTS charts (
        chart_id SERIAL PRIMARY KEY,
        date DATE NOT NULL,
        song_id INT REFERENCES songs(song_id) ON DELETE CASCADE,
        position INT NOT NULL,
        platform_id INT REFERENCES platforms(platform_id) ON DELETE SET NULL
    );

    -- Create rankings table
    CREATE TABLE IF NOT EXISTS rankings (
        ranking_id SERIAL PRIMARY KEY,
        song_id INT REFERENCES songs(song_id) ON DELETE CASCADE,
        platform_id INT REFERENCES platforms(platform_id) ON DELETE SET NULL,
        year INT NOT NULL,
        rank INT NOT NULL,
        UNIQUE (song_id, platform_id, year)  -- Ensure unique ranking per song per year per platform
    );
EOSQL
