CREATE KEYSPACE IF NOT EXISTS plannet WITH REPLICATION={'class':'SimpleStrategy', 'replication_factor':3};

USE plannet;

CREATE TYPE plannet.achieve
(
    type text,
    created_at timestamp
);

CREATE TYPE plannet.room
(
    name text,
    category text,
    level int,
    exp int,
    max_num int
);

CREATE TABLE plannet.users
(
    category text,
    email text,
    name text,
    exp int,
    interests list<text>,
    achieves list<frozen<achieve>>,
    doing list<frozen<room>>,
    done list<frozen<room>>,
    evaluate map<text, int>,
    created_at timestamp,
    PRIMARY KEY (category, email)
);

CREATE TYPE plannet.user
(
    name text,
    penalty text,
    attendance list<timestamp>,
    todo map<text, boolean>
);

CREATE TABLE plannet.rooms
(
    category text,
    name text,
    description text,
    level int,
    exp int,
    status text,
    captain map<text, frozen<user>>,
    crew map<text, frozen<user>>,
    max_penalty int,
    progress int,
    attendance list<timestamp>,
    link text,
    created_at timestamp,
    PRIMARY KEY (category, name)
);

select * from system_schema.tables where keyspace_name='plannet';