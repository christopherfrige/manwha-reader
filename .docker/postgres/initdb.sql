CREATE DATABASE IF NOT EXISTS manwha_reader;

USE manwha_reader;

CREATE SCHEMA IF NOT EXISTS manwha;
CREATE SCHEMA IF NOT EXISTS chapter;
CREATE SCHEMA IF NOT EXISTS alternative_name;
CREATE SCHEMA IF NOT EXISTS artist;
CREATE SCHEMA IF NOT EXISTS author;
CREATE SCHEMA IF NOT EXISTS genre;

-- Entity tables

CREATE TABLE IF NOT EXISTS manwha.manwha (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS chapter.chapter (
    id SERIAL PRIMARY KEY,
    manwha_id INT NOT NULL,
    chapter_number FLOAT NOT NULL,
    pages INT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP,
    FOREIGN KEY (manwha_id)
        REFERENCES manwha.manwha (id),
);

CREATE TABLE IF NOT EXISTS alternative_name.alternative_name (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS genre.genre (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS artist.artist (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS author.author (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP
);

-- Junction tables

CREATE TABLE IF NOT EXISTS manwha.manwha_chapter (
    manwha_id INT NOT NULL,
    chapter_id INT NOT NULL,
    PRIMARY KEY (manwha_id, chapter_id),
    FOREIGN KEY (manwha_id)
        REFERENCES manwha.manwha (id),
    FOREIGN KEY (chapter_id)
        REFERENCES chapter.chapter (id)
);

CREATE TABLE IF NOT EXISTS manwha.manwha_alternative_name (
    manwha_id INT NOT NULL,
    alternative_name_id INT NOT NULL,
    PRIMARY KEY (manwha_id, chapter_id),
    FOREIGN KEY (manwha_id)
        REFERENCES manwha.manwha (id),
    FOREIGN KEY (alternative_name_id)
        REFERENCES alternative_name.alternative_name (id)
);

CREATE TABLE IF NOT EXISTS manwha.manwha_genre (
    manwha_id INT NOT NULL,
    genre_id INT NOT NULL,
    PRIMARY KEY (manwha_id, chapter_id),
    FOREIGN KEY (manwha_id)
        REFERENCES manwha.manwha (id),
    FOREIGN KEY (genre_id)
        REFERENCES genre.genre (id)
);

CREATE TABLE IF NOT EXISTS manwha.manwha_author (
    manwha_id INT NOT NULL,
    author_id INT NOT NULL,
    PRIMARY KEY (manwha_id, chapter_id),
    FOREIGN KEY (manwha_id)
        REFERENCES manwha.manwha (id),
    FOREIGN KEY (author_id)
        REFERENCES author.author (id)
);

CREATE TABLE IF NOT EXISTS manwha.manwha_artist (
    manwha_id INT NOT NULL,
    artist_id INT NOT NULL,
    PRIMARY KEY (manwha_id, chapter_id),
    FOREIGN KEY (manwha_id)
        REFERENCES manwha.manwha (id),
    FOREIGN KEY (artist_id)
        REFERENCES artist.artist (id)
);

