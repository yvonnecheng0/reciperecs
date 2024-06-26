from flask import Flask, request, redirect, url_for, render_template
import db
from recipe import get_recipes

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <h1>Recipe Finder</h1>
    <form action="/submit" method="post">
        <label for="ingredients">Enter your ingredients (comma-separated):</label>
        <input type="text" name="ingredients" id="ingredients" required>
        <button type="submit">Find Recipes</button>
    </form>
    <a href="/stored_recipes">View Stored Recipes</a>
    '''

@app.route('/submit', methods=['POST'])
def submit():
    ingredients = request.form.get('ingredients').split(',')
    ingredients = [ingredient.strip() for ingredient in ingredients]
    for ingredient in ingredients:
        db.add_ingredient(ingredient)
    recipes = get_recipes(ingredients)
    
    for recipe in recipes:
        name = recipe['title']
        url = recipe['sourceUrl']
        db.save_recipe(name, url)

    return redirect(url_for('stored_recipes'))

@app.route('/stored_recipes')
def stored_recipes():
    recipes = db.get_stored_recipes()
    return render_template('stored_recipes.html', recipes=recipes)

@app.route('/submit', methods=['GET'])
def handle_get_submit():
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_database()
    app.run(debug=True)
