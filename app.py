from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


@app.route("/")
def index():
    mars_data = mongo.db.collection.find_one()
    print(mars_data)
    return render_template("index.html", mars_dict=mars_data)


@app.route("/scrape")
def scraper():
    # mars_dict = mongo.db.collection
    mars_dict_data = scrape_mars.scrape()
    mongo.db.collection.replace_one({}, mars_dict_data, upsert=True)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
