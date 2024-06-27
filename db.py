import sqlite3

# Initialize database and create ingredients and recipes tables
def create_database():
    conn = sqlite3.connect('ingredients.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS ingredients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipe_id INTEGER NOT NULL,
            title TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Save a list of ingredients to database
def get_ingredients():
    conn = sqlite3.connect('ingredients.db')
    c = conn.cursor()
    c.execute('SELECT name FROM ingredients')
    ingredients = [row[0] for row in c.fetchall()]
    conn.close()
    return ingredients

# Add a single ingredient to the database
def add_ingredient(name):
    conn = sqlite3.connect('ingredients.db')
    c = conn.cursor()
    c.execute('INSERT INTO ingredients (name) VALUES (?)', (name,))
    conn.commit()
    conn.close()

# Save a recipe and its ingredients to the database
def save_recipe(recipe):
    conn = sqlite3.connect('ingredients.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO recipes (recipe_id, title) VALUES (?, ?)", (recipe['id'], recipe['title']))
    conn.commit()
    conn.close()

# Get all stored recipes from the database
def get_stored_recipes():
    conn = sqlite3.connect('ingredients.db')
    cursor = conn.cursor()
    cursor.execute("SELECT recipe_id, title FROM recipes")
    recipes = cursor.fetchall()
    conn.close()
    return recipes

# Initialize database
create_database()
