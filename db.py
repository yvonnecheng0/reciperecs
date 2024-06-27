import sqlite3

def create_database():
    """
    Create the SQLite database and the necessary tables if they do not exist.
    """
    conn = sqlite3.connect('recipes.db')
    c = conn.cursor()
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS ingredients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            url TEXT NOT NULL,
            UNIQUE(title, url)
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS recipe_ingredients (
            recipe_id INTEGER,
            ingredient_id INTEGER,
            FOREIGN KEY (recipe_id) REFERENCES recipes(id),
            FOREIGN KEY (ingredient_id) REFERENCES ingredients(id),
            UNIQUE (recipe_id, ingredient_id)
        )
    ''')

    conn.commit()
    conn.close()

def add_ingredient(name):
    """
    Add a single ingredient to the ingredients table or retrieve its ID if it exists.
    """
    conn = sqlite3.connect('recipes.db')
    c = conn.cursor()
    c.execute('SELECT id FROM ingredients WHERE name = ?', (name,))
    row = c.fetchone()
    if row:
        ingredient_id = row[0]
    else:
        c.execute('INSERT INTO ingredients (name) VALUES (?)', (name,))
        ingredient_id = c.lastrowid
    conn.commit()
    conn.close()
    return ingredient_id

def add_recipe(title, url):
    """
    Add a single recipe to the recipes table or retrieve its ID if it exists.
    """
    conn = sqlite3.connect('recipes.db')
    c = conn.cursor()
    c.execute('SELECT id FROM recipes WHERE title = ? AND url = ?', (title, url))
    row = c.fetchone()
    if row:
        recipe_id = row[0]
    else:
        c.execute('INSERT INTO recipes (title, url) VALUES (?, ?)', (title, url))
        recipe_id = c.lastrowid
    conn.commit()
    conn.close()
    return recipe_id

def add_recipe_ingredient(recipe_id, ingredient_id):
    """
    Associate an ingredient with a recipe in the recipe_ingredients table.
    """
    conn = sqlite3.connect('recipes.db')
    c = conn.cursor()
    c.execute('SELECT * FROM recipe_ingredients WHERE recipe_id = ? AND ingredient_id = ?', (recipe_id, ingredient_id))
    row = c.fetchone()
    if not row:
        c.execute('INSERT INTO recipe_ingredients (recipe_id, ingredient_id) VALUES (?, ?)', (recipe_id, ingredient_id))
    conn.commit()
    conn.close()

def get_ingredients():
    """
    Retrieve all ingredients from the ingredients table.
    """
    conn = sqlite3.connect('recipes.db')
    c = conn.cursor()
    c.execute('SELECT DISTINCT name FROM ingredients')
    ingredients = [row[0] for row in c.fetchall()]
    conn.close()
    return ingredients

def get_recipes_with_ingredients():
    """
    Retrieve all recipes along with their associated ingredients.
    """
    conn = sqlite3.connect('recipes.db')
    c = conn.cursor()
    c.execute('''
        SELECT recipes.title, recipes.url, GROUP_CONCAT(DISTINCT ingredients.name)
        FROM recipes
        JOIN recipe_ingredients ON recipes.id = recipe_ingredients.recipe_id
        JOIN ingredients ON recipe_ingredients.ingredient_id = ingredients.id
        GROUP BY recipes.id
    ''')
    recipes = [{'title': row[0], 'url': row[1], 'ingredients': row[2].split(',')} for row in c.fetchall()]
    conn.close()
    return recipes

def clear_database():
    """
    Clear all data from the database.
    """
    conn = sqlite3.connect('recipes.db')
    c = conn.cursor()
    c.execute('DELETE FROM recipe_ingredients')
    c.execute('DELETE FROM recipes')
    c.execute('DELETE FROM ingredients')
    conn.commit()
    conn.close()

# Initialize the database by creating the tables.
create_database()

