from flask import Flask, request, render_template, redirect, url_for, flash
import db
import recipe
import secrets
import git

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Ensure this is a secure key

# Make home page with form to enter ingredients
@app.route('/')
def index():
    return render_template('index.html')

# Handle form submission, save ingredients to the database,
# fetch recipes based on the ingredients, and render results page
@app.route('/submit', methods=['POST'])
def submit():
    ingredients = request.form.getlist('ingredients[]')
    if not ingredients or all(ing.strip() == "" for ing in ingredients):
        flash('Please enter at least one ingredient.')
        return redirect(url_for('index'))

    for ingredient in ingredients:
        if ingredient.strip():
            db.add_ingredient(ingredient.strip())
    recipes = recipe.new_get_recipes(ingredients)
    return render_template('results.html', recipes=recipes)


# Render results page with saved recipes and ingredients
@app.route('/results')
def results():
    recipes = db.get_recipes_with_ingredients()
    return render_template('results.html', recipes=recipes)

@app.route('/history')
def history():
    recipes = db.get_recipes_with_nutrition()
    return render_template('history.html', recipes=recipes)

@app.route('/nutrition')
def nutrition():
    recipes = db.get_recipes_with_nutrition()
    return render_template('nutrition.html', recipes=recipes)

''' # Clear all data from database
@app.route("/update_server", methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('/home/ANYWHERE_USERNAME/REPO_NAME')
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400
'''
# Clear all data from database
@app.route('/clear', methods=['POST'])
def clear():
    db.clear_database()
    flash('Database cleared successfully.')
    return redirect(url_for('index'))

# Redirect GET requests for /submit to the home page
@app.route('/submit', methods=['GET'])
def handle_get_submit():
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_database()  
    app.run(debug=True)