import sqlite3

#Initialize database and create ingredients table
def create_database():
    conn = sqlite3.connect('ingredients.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS ingredients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipe_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            image TEXT NOT NULL
        )
    ''')
#Save a list of ingredients to database
def get_ingredients():
    conn = sqlite3.connect('ingredients.db')
    c = conn.cursor()
    c.execute('SELECT name FROM ingredients')
    ingredients = [row[0] for row in c.fetchall()]
    conn.close()
    return ingredients
    
def add_ingredient(name):
    conn = sqlite3.connect('ingredients.db')
    c = conn.cursor()
    c.execute('INSERT INTO ingredients (name) VALUES (?)', (name,))
    conn.commit()
    conn.close()
    
def add_recipe(recipe_id, title, image):
    conn = sqlite3.connect('ingredients.db')
    c = conn.cursor()
    c.execute('INSERT INTO recipes (recipe_id, title, image) VALUES (?, ?, ?)', (recipe_id, title, image))
    conn.commit()
    conn.close()

def get_stored_recipes():
    conn = sqlite3.connect('ingredients.db')
    c = conn.cursor()
    c.execute('SELECT recipe_id, title, image FROM recipes')
    recipes = [{'id': row[0], 'title': row[1], 'image': row[2]} for row in c.fetchall()]
    conn.close()
    return recipes

#Intialize database 
create_database()



