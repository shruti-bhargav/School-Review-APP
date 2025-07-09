CREATE DATABASE IF NOT EXISTS school_reviews;

USE school_reviews;
CREATE TABLE IF NOT EXISTS reviews(
    id INT AUTO_INCREMENT PRIMARY KEY,
    school_name VARCHAR NOT NULL;
    rating VARCHAR NOT NULL;
    review_text TEXT NOT NULL
);