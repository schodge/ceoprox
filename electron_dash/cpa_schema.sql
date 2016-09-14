CREATE TABLE battery
(
    entry integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    device text,
    ts text,
    capacity double precision
);

CREATE TABLE position
(
    entry integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    device text,
    ts text,
    lat double precision,
    lon double precision
);
