CREATE KEYSPACE IF NOT EXISTS plannet WITH REPLICATION={'class':'SimpleStrategy', 'replication_factor':3};

USE plannet;

CREATE TABLE plannet.users
(
    email text,
    name text,
    exp int,
    interests list<text>,
    achieve map<text, timestamp>,
    room map<text, boolean>,
    evaluate list<text>,
    created_at timestamp,
    PRIMARY KEY (email)
);

CREATE TABLE plannet.rooms
(
    category text,
    name text,
    description text,
    level int,
    exp int,
    status text,
    captain map<text, text>,
    crew map<text, text>,
    max_penalty int,
    progress int,
    link text,
    created_at timestamp,
    PRIMARY KEY (category, name)
);

CREATE TABLE plannet.attendance
(
    category text,
    name text,
    attend_at date,
    attendee list<text>,
    PRIMARY KEY ((category, name), attend_at)
);

CREATE TABLE plannet.penalty
(
    category text,
    name text,
    email text,
    penalty counter,
    PRIMARY KEY (category, name, email)
);

CREATE TABLE plannet.todo
(
    category text,
    name text,
    email text,
    todo text,
    done boolean,
    PRIMARY KEY ((category, name, email), todo)
);
