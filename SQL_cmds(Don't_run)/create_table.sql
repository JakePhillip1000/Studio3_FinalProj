CREATE TABLE IF NOT EXISTS athletes (
    id BIGINT PRIMARY KEY,
    country VARCHAR(5) NOT NULL,
    "firstName" VARCHAR(100) NOT NULL,
    "lastName" VARCHAR(100) NOT NULL,
    gender VARCHAR(10) NOT NULL,
    "dateOfBirth" DATE,
    classification VARCHAR(50),
    "imgProfile" VARCHAR(255),
    email VARCHAR(254)
);


