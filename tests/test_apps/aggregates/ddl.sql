CREATE TABLE P1 (
    P1PK       BIGINT NOT NULL,
    INT1        INTEGER,
    VARCHAR1    VARCHAR(1000),
    PRIMARY KEY(P1PK));

CREATE TABLE P2 (
    P2PK       BIGINT NOT NULL,
    P1FK       BIGINT NOT NULL,
    INT1        INTEGER,
    VARCHAR1    VARCHAR(1000),
    PRIMARY KEY(P2PK));


