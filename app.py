from flask import Flask , render_template , request , redirect
import mysql.connector
import config

app= Flask(__name__)
db=mysql.connector.connect(
    host=config.DB_HOST ,
    user=config.DB_USER ,
    password=config.DB_PASSWORD,
    database=config.DB_NAME
)

cursor=db.cursor()

@app.route('/')
def home():
    return render_template("add_review_html")

@app.route('/submit/' , methods=["post"])
def submit():
    school=request.form['school']
    rating=request.form['rating']
    review=request.form['review']


    query=" INSERT INTO reviews(school_name,rating,review_text) VALUESA (%s,%s,%s)"
    values=(school,rating,review)
    cursor.execute(query,values)
    db.commit()


    @app.route('/review/')
    def reviews():
        cursor.execute("SELECT * FROM reviews")
        all_reviews=cursor.fetchall()
        return render_template("reviews.html")

if __name__=="__main__":
    app.run(debug=True)


