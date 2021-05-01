CREATE DATABASE audio;
\c audio;

BEGIN;

CREATE TABLE song (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    duration INTEGER CHECK (duration > 0),
    upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL -- auto create on insertion
);

CREATE TABLE podcast (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    duration INTEGER CHECK (duration > 0),
    upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL, -- auto create on insertion
    host VARCHAR(100) NOT NULL,
    participants VARCHAR(100) ARRAY[10] CHECK(array_length(participants, 1) <=10)
);

CREATE TABLE audiobook (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    author VARCHAR(100) NOT NULL,
    narrator VARCHAR(100) NOT NULL,
    duration INTEGER CHECK (duration > 0),
    upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL -- auto create on insertion
);

COMMIT;