--
-- File generated with SQLiteStudio v3.4.20 on So Jan 18 19:59:51 2026
--
-- Text encoding used: System
--

PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: kunden
DROP TABLE IF EXISTS kunden;

CREATE TABLE IF NOT EXISTS kunden (
    Id       INTEGER PRIMARY KEY AUTOINCREMENT
                     NOT NULL,
    vorname  TEXT    NOT NULL,
    nachname TEXT    NOT NULL,
    email    TEXT    NOT NULL
);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
