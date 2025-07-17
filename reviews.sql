DROP TABLE IF EXISTS reviews;

CREATE TABLE reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100),
    email VARCHAR(100),
    school_name VARCHAR(255) NOT NULL,
    rating VARCHAR(10) NOT NULL,
    review_text TEXT NOT NULL,
    date_submitted DATETIME DEFAULT CURRENT_TIMESTAMP
);