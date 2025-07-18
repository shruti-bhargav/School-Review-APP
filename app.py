


from flask import Flask, render_template, request, redirect
import mysql.connector
import config

app = Flask(__name__)


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
    full_name = request.form['full_name']
    email = request.form['email']
    school = request.form['school']
    rating = request.form['rating']
    review = request.form['review']

    query = "INSERT INTO reviews (full_name, email,school_name, rating, review_text) VALUES (%s, %s, %s,%s,%s)"
    values = (full_name, email, school, rating, review)
    cursor.execute(query, values)
    db.commit()
    print("Form submitted")
    return redirect('/review')



@app.route("/review")
def review():
    cursor.execute("SELECT * FROM reviews ORDER BY id DESC")

    
    all_reviews = cursor.fetchall()
    return render_template("reviews.html", all_reviews=all_reviews)




@app.route('/search')
def search_review():
    query = request.args.get('query', '').strip()
    if not query:
        return redirect('/review')

    sql = """ SELECT * FROM reviews WHERE LOWER(school_name) LIKE LOWER(%s) OR LOWER(email) LIKE LOWER(%s) ORDER BY id DESC """
    like_param = '%' + query + '%'
    cursor.execute(sql, (like_param, like_param))
    all_reviews = cursor.fetchall()
    return render_template('reviews.html', all_reviews=all_reviews)






if __name__ == "__main__":
    app.run(debug=True)


