from flask import Flask, request, flash
from flask import render_template, redirect, url_for
import db
from recipe import get_recipes
import secrets

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
    if not ingredients or all(not ing.strip() for ing in ingredients):
        flash('Please enter at least one ingredient.')
        return redirect(url_for('index'))
    recipes = get_recipes(ingredients)
    return redirect(url_for('results'))


#Make results page with saved recipes and ingredients
@app.route('/results')
def results():
    recipes = db.get_recipes_with_ingredients()
    return render_template('results.html', recipes=recipes)

#Clear data from database
@app.route('/clear', methods=['POST'])
def clear():
    db.clear_database()
    flash('Database cleared successfully.')
    return redirect(url_for('index'))

#Redirect GET requests for /submit to home page
@app.route('/submit', methods=['GET'])
def handle_get_submit():
    return redirect(url_for('index'))

if __name__ == '__main__':
    #Initialize database and run Flask app in debug mode
    db.create_database()
    app.run(debug=True)

