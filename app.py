


from flask import Flask, render_template, request, redirect
import mysql.connector
import config

app = Flask(__name__)

# Database connection
db = mysql.connector.connect(
    host=config.DB_HOST,
    user=config.DB_USER,
    password=config.DB_PASSWORD,
    database=config.DB_NAME
)
cursor = db.cursor()

@app.route('/')
def home():
    return render_template("add_review.html", all_reviews=[])

@app.route('/submit/', methods=["POST"])
def submit():
    school = request.form['school']
    rating = request.form['rating']
    review = request.form['review']

    query = "INSERT INTO reviews (school_name, rating, review_text) VALUES (%s, %s, %s)"
    values = (school, rating, review)
    cursor.execute(query, values)
    db.commit()
    print("Form submitted")
    return redirect('/review/')

@app.route('/review/')
def reviews():
    cursor.execute("SELECT * FROM reviews")
    all_reviews = cursor.fetchall()
    return render_template("add_review.html", all_reviews=all_reviews)

if __name__ == "__main__":
    app.run(debug=True)


