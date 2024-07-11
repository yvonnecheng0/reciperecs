from flask import Flask, request, flash
from flask import render_template, redirect, url_for
import db
import recipe
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Ensure this is a secure key

#Render home page with form to enter ingredients 
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    ingredients = request.form.getlist('ingredients[]')
    if not ingredients or all(ing.strip() == "" for ing in ingredients):
        flash('Please enter at least one ingredient.')
        return redirect(url_for('index'))

    for ingredient in ingredients:
        if ingredient.strip():
            db.add_ingredient(ingredient.strip())
    recipes = recipe.get_recipes(ingredients)
    return render_template('results.html', recipes=recipes)

@app.route('/clear', methods=['POST'])
def clear():
    db.clear_database()
    flash('Database cleared.')
    return redirect(url_for('index'))

@app.route('/submit', methods=['GET'])
def handle_get_submit():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)














