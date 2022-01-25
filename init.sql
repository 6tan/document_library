CREATE DATABASE document;
\c audio;

BEGIN;

CREATE TABLE tbl_users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    access_token uuid default uuid_generate_v4() not null unique, -- unique id assigned to user
    joined timestamp with time zone not null default current_timestamp NOT NULL -- auto create on insertion
);

CREATE TABLE tbl_document (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    data BYTEA NOT NULL,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL, -- auto create on insertion
    lock BOOLEAN DEFAULT FALSE,
    shared_users INT ARRAY[],
    last_updated
    CONSTRAINT fk_user_id  FOREIGN KEY(user_id)  REFERENCES tbl_users(id)
);

CREATE TABLE tbl_history (
    id SERIAL PRIMARY KEY,
    document_id VARCHAR(100) NOT NULL,
    owner INTEGER NOT NULL,
    editor INTEGER NOT NULL,
    action VARCHAR(20) NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL, -- auto create on insertion
    CONSTRAINT fk_document_id  FOREIGN KEY(document_id)  REFERENCES tbl_document(id),
    CONSTRAINT fk_owner_id  FOREIGN KEY(owner)  REFERENCES tbl_users(id),
    CONSTRAINT fk_editor_id  FOREIGN KEY(editor)  REFERENCES tbl_users(id),
);

COMMIT;