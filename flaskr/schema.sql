DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS comment;
DROP TABLE IF EXISTS artist;
DROP TABLE IF EXISTS track;
DROP TABLE IF EXISTS friend;
DROP TABLE IF EXISTS book;
/*
CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE comment (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  post TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);
*/
CREATE TABLE artist (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  image_url TEXT NOT NULL,
  spotify_url TEXT NOT NULL,
  rank INTEGER UNIQUE NOT NULL
);

CREATE TABLE track (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  artist TEXT NOT NULL,
  spotify_url TEXT NOT NULL,
  rank INTEGER UNIQUE NOT NULL
);

CREATE TABLE friend (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  birthday DATE NOT NULL
);

CREATE TABLE book (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  author TEXT NOT NULL,
  status TEXT NOT NULL,
  url TEXT NOT NULL
);