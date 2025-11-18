CREATE TABLE IF NOT EXISTS User (
    id CHAR(36) PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255),
    is_admin BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS Place (
    id CHAR(36) PRIMARY KEY,
    title VARCHAR(255),
    description TEXT,
    price DECIMAL(10, 2),
    latitude FLOAT,
    longitude FLOAT,
    owner_id CHAR(36),
    FOREIGN KEY (owner_id) REFERENCES User(id)
);

CREATE TABLE IF NOT EXISTS Review (
    id CHAR(36) PRIMARY KEY,
    text TEXT,
    rating INT CHECK (rating >= 1 AND rating <= 5),
    user_id CHAR(36),
    place_id CHAR(36),
    FOREIGN KEY (user_id) REFERENCES User(id),
    FOREIGN KEY (place_id) REFERENCES Place(id),
    CONSTRAINT unique_review_place UNIQUE (user_id, place_id)
);

CREATE TABLE IF NOT EXISTS Amenity(
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) UNIQUE
);

CREATE TABLE IF NOT EXISTS Place_Amenity(
    place_id CHAR(36),
    amenity_id CHAR(36),
    PRIMARY KEY(place_id, amenity_id),
    FOREIGN KEY (place_id) REFERENCES Place(id),
    FOREIGN KEY (amenity_id) REFERENCES Amenity(id)
);

INSERT OR IGNORE INTO User (id, first_name, last_name, email, password, is_admin)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.com',
    '$2b$12$VdHyFNE57jk1BhkhiJN0/O8fvaBiC9GtBMROr6rMD/6wpoQ0hLKs6',
    TRUE
);

INSERT OR IGNORE INTO Amenity (id, name) VALUES
('11111111-1111-1111-1111-111111111111', 'WiFi'),
('22222222-2222-2222-2222-222222222222', 'Swimming Pool'),
('33333333-3333-3333-3333-333333333333', 'Air Conditioning');