CREATE TABLE songs (
    id SERIAL PRIMARY KEY,
    rank VARCHAR(10),
    title VARCHAR(255),
    artist VARCHAR(255),
    distribution_date VARCHAR(255)  -- Add this line
);
