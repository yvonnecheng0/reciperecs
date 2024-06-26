from flask import Flask, request
from flask import render_template, redirect, url_for
import db
from recipe import get_recipes

app = Flask(__name__)

#Render home page with form to enter ingredients 
@app.route('/')
def index():
    return render_template('index.html')

#Handle submission form, save ingredients to database,
#fetch top 5 recipes, and return results
@app.route('/submit', methods=['POST'])
def submit():
    ingredients = request.form.getlist('ingredients[]')
    for ingredient in ingredients:
        db.get_ingredients()
    recipes = get_recipes(ingredients)
    return render_template('results.html', recipes=recipes)

#Redirect GET requests for /submit to home page
@app.route('/submit', methods=['GET'])
def handle_get_submit():
    return redirect(url_for('index'))

if __name__ == '__main__':
    #Initialize database and run Flask app in debug mode
    db.create_database()
    app.run(debug=True)

