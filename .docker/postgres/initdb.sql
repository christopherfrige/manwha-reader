CREATE SCHEMA IF NOT EXISTS manwha;
CREATE SCHEMA IF NOT EXISTS chapter;
CREATE SCHEMA IF NOT EXISTS alternative_name;
CREATE SCHEMA IF NOT EXISTS artist;
CREATE SCHEMA IF NOT EXISTS author;
CREATE SCHEMA IF NOT EXISTS genre;
CREATE SCHEMA IF NOT EXISTS scraper;

-- Entity tables

CREATE TABLE IF NOT EXISTS manwha.manwha (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    thumbnail TEXT,
    summary TEXT,
    release TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS chapter.chapter (
    id SERIAL PRIMARY KEY,
    manwha_id INT NOT NULL,
    chapter_number FLOAT NOT NULL,
    pages INT NOT NULL,
    origin_url TEXT,
    downloaded BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (manwha_id)
        REFERENCES manwha.manwha (id)
);

CREATE TABLE IF NOT EXISTS alternative_name.alternative_name (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS genre.genre (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS artist.artist (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS author.author (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS scraper.reader (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS scraper.manwha (
    id SERIAL PRIMARY KEY,
    reader_id INT NOT NULL,
    manwha_id INT,
    url TEXT NOT NULL,
    chapter_start INT NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (reader_id)
        REFERENCES scraper.reader (id),
    FOREIGN KEY (manwha_id)
        REFERENCES manwha.manwha (id)
);

-- Junction tables

CREATE TABLE IF NOT EXISTS manwha.manwha_alternative_name (
    manwha_id INT NOT NULL,
    alternative_name_id INT NOT NULL,
    PRIMARY KEY (manwha_id, alternative_name_id),
    FOREIGN KEY (manwha_id)
        REFERENCES manwha.manwha (id),
    FOREIGN KEY (alternative_name_id)
        REFERENCES alternative_name.alternative_name (id)
);

CREATE TABLE IF NOT EXISTS manwha.manwha_genre (
    manwha_id INT NOT NULL,
    genre_id INT NOT NULL,
    PRIMARY KEY (manwha_id, genre_id),
    FOREIGN KEY (manwha_id)
        REFERENCES manwha.manwha (id),
    FOREIGN KEY (genre_id)
        REFERENCES genre.genre (id)
);

CREATE TABLE IF NOT EXISTS manwha.manwha_author (
    manwha_id INT NOT NULL,
    author_id INT NOT NULL,
    PRIMARY KEY (manwha_id, author_id),
    FOREIGN KEY (manwha_id)
        REFERENCES manwha.manwha (id),
    FOREIGN KEY (author_id)
        REFERENCES author.author (id)
);

CREATE TABLE IF NOT EXISTS manwha.manwha_artist (
    manwha_id INT NOT NULL,
    artist_id INT NOT NULL,
    PRIMARY KEY (manwha_id, artist_id),
    FOREIGN KEY (manwha_id)
        REFERENCES manwha.manwha (id),
    FOREIGN KEY (artist_id)
        REFERENCES artist.artist (id)
);

CREATE FUNCTION set_updated_at() RETURNS trigger AS $$
BEGIN
  NEW.updated_at := CURRENT_TIMESTAMP;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers

CREATE TRIGGER set_updated_at
BEFORE UPDATE ON manwha.manwha
FOR EACH ROW EXECUTE PROCEDURE set_updated_at();

CREATE TRIGGER set_updated_at
BEFORE UPDATE ON chapter.chapter
FOR EACH ROW EXECUTE PROCEDURE set_updated_at();

CREATE TRIGGER set_updated_at
BEFORE UPDATE ON genre.genre
FOR EACH ROW EXECUTE PROCEDURE set_updated_at();

CREATE TRIGGER set_updated_at
BEFORE UPDATE ON alternative_name.alternative_name
FOR EACH ROW EXECUTE PROCEDURE set_updated_at();

CREATE TRIGGER set_updated_at
BEFORE UPDATE ON author.author
FOR EACH ROW EXECUTE PROCEDURE set_updated_at();

CREATE TRIGGER set_updated_at
BEFORE UPDATE ON scraper.reader
FOR EACH ROW EXECUTE PROCEDURE set_updated_at();

CREATE TRIGGER set_updated_at
BEFORE UPDATE ON scraper.manwha
FOR EACH ROW EXECUTE PROCEDURE set_updated_at();

-- Inserts

INSERT INTO scraper.reader (id, name) VALUES (1, 'Inari');
