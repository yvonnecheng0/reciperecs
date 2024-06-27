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
    query = request.form['query']
    recipes = get_recipes(query)
    conn = get_db_connection()
    for recipe in recipes:
        save_recipe(conn, recipe)
    conn.close()
    return redirect(url_for('stored_recipes', recipes=recipes))

@app.route('/stored_recipes')
def stored_recipes():
    conn = get_db_connection()
    recipes = get_stored_recipes(conn)
    conn.close()
    return render_template('stored_recipes.html', recipes=recipes)

@app.route('/submit', methods=['GET'])
def handle_get_submit():
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_database()
    app.run(debug=True)
