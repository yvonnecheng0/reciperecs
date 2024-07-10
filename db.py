import sqlite3
import json

def create_database():
    conn = sqlite3.connect('recipes.db')
    c = conn.cursor()
    
    # Create ingredients table
    c.execute('''
        CREATE TABLE IF NOT EXISTS ingredients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    ''')

    # Create recipes table with the nutrition_info column
    c.execute('''
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            url TEXT NOT NULL,
            nutrition_info TEXT,
            UNIQUE(title, url)
        )
    ''')

    # Create recipe_ingredients table
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
    conn = sqlite3.connect('recipes.db')
    c = conn.cursor()
    
    c.execute('INSERT OR IGNORE INTO ingredients (name) VALUES (?)', (name,))
    c.execute('SELECT id FROM ingredients WHERE name = ?', (name,))
    ingredient_id = c.fetchone()[0]
    
    conn.commit()
    conn.close()
    return ingredient_id

def add_recipe(title, url):
    conn = sqlite3.connect('recipes.db')
    c = conn.cursor()
    
    c.execute('INSERT OR IGNORE INTO recipes (title, url) VALUES (?, ?)', (title, url))
    c.execute('SELECT id FROM recipes WHERE title = ? AND url = ?', (title, url))
    recipe_id = c.fetchone()[0]
    
    conn.commit()
    conn.close()
    return recipe_id

def add_recipe_ingred(recipe_id, ingredient_id):
    conn = sqlite3.connect('recipes.db')
    c = conn.cursor()
    
    c.execute('INSERT OR IGNORE INTO recipe_ingredients (recipe_id, ingredient_id) VALUES (?, ?)', (recipe_id, ingredient_id))
    
    conn.commit()
    conn.close()

def get_ingredients():
    conn = sqlite3.connect('recipes.db')
    c = conn.cursor()
    
    c.execute('SELECT DISTINCT name FROM ingredients')
    ingredients = [row[0] for row in c.fetchall()]
    
    conn.close()
    return ingredients

def get_recipes_with_ingredients():
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

def save_nutrition_info(recipe_id, nutrition_info):
    conn = sqlite3.connect('recipes.db')
    c = conn.cursor()
    print(f"Saving nutrition info for recipe_id {recipe_id}: {nutrition_info}")  # Debug print
    c.execute('UPDATE recipes SET nutrition_info = ? WHERE id = ?', (json.dumps(nutrition_info), recipe_id))
    conn.commit()
    conn.close()

def get_recipes_with_nutrition():
    conn = sqlite3.connect('recipes.db')
    c = conn.cursor()
    
    c.execute('''
        SELECT recipes.title, recipes.url, recipes.nutrition_info, GROUP_CONCAT(DISTINCT ingredients.name)
        FROM recipes
        JOIN recipe_ingredients ON recipes.id = recipe_ingredients.recipe_id
        JOIN ingredients ON recipe_ingredients.ingredient_id = ingredients.id
        GROUP BY recipes.id
    ''')
    
    recipes = []
    for row in c.fetchall():
        title = row[0]
        url = row[1]
        nutrition_info = json.loads(row[2]) if row[2] else []
        ingredient_names = row[3].split(',')
        
        recipes.append({
            'title': title,
            'url': url,
            'ingredients': ingredient_names,
            'nutrition': nutrition_info
        })
    
    conn.close()
    return recipes

def clear_database():
    conn = sqlite3.connect('recipes.db')
    c = conn.cursor()
    
    c.execute('DELETE FROM recipe_ingredients')
    c.execute('DELETE FROM recipes')
    c.execute('DELETE FROM ingredients')
    
    conn.commit()
    conn.close()

create_database()