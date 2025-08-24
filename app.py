from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os
from urllib.parse import urlparse

app = Flask(__name__)
app.secret_key = "supersecretkey"



# --- Database Connection ---

from urllib.parse import urlparse

def get_db_connection():
    # Parse the DATABASE_URL
    url = urlparse(os.environ.get("DATABASE_URL"))
    
    return mysql.connector.connect(
        host=url.hostname,
        user=url.username,
        password=url.password,
        database=url.path[1:],  
        port=url.port
    )

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INT AUTO_INCREMENT PRIMARY KEY,
            school_name VARCHAR(255) NOT NULL,
            full_name VARCHAR(255) NOT NULL,
            rating INT NOT NULL,
            email VARCHAR(255),
            review_text TEXT
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

init_db()


# --- Home Page / List All Reviews ---
@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM reviews ORDER BY id DESC")
    reviews = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('reviews.html', reviews=reviews)

# --- Add Review ---
@app.route("/add", methods=["GET", "POST"])
def add_review():
    if request.method == "POST":
        school_name = request.form["school_name"]
        full_name = request.form["full_name"]  # Changed to full_name
        rating = request.form["rating"]
        email = request.form["email"]
        review_text = request.form["review_text"]

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO reviews (school_name, full_name, rating, email, review_text) VALUES (%s, %s, %s, %s, %s)",
            (school_name, full_name, rating, email, review_text)  # Changed to full_name
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for("index"))
    return render_template("add_review.html")

# --- Edit Review ---
@app.route("/edit/<int:review_id>", methods=["GET", "POST"])
def edit_review(review_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        school_name = request.form["school_name"]
        full_name = request.form["full_name"]  # Changed to full_name
        rating = request.form["rating"]
        email = request.form["email"]
        review_text = request.form["review_text"]

        cursor.execute(
            "UPDATE reviews SET school_name=%s, full_name=%s, rating=%s, email=%s, review_text=%s WHERE id=%s",
            (school_name, full_name, rating, email, review_text, review_id)  # Changed to full_name
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for("index"))

    cursor.execute("SELECT * FROM reviews WHERE id=%s", (review_id,))
    review = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template("edit_reviews.html", review=review)

# --- Delete Review ---
@app.route("/delete/<int:review_id>", methods=["POST"])
def delete_review(review_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM reviews WHERE id=%s", (review_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    port=int(os.environ.get("PORT" , 5000))
    app.run(host="0.0.0.0" , port=port , debug=True)