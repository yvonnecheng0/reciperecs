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
    c.execute('''
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipe_id INTEGER NOT NULL,
            title TEXT NOT NULL,
        )
    ''')
    conn.commit()
    conn.close()
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
    
def save_recipe(conn, recipe):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO recipes (recipe_id, title) VALUES (?, ?)", (recipe['id'], recipe['title']))
    for ingredient in recipe['ingredients']:
        cursor.execute("INSERT INTO ingredients (recipe_id, name) VALUES (?, ?)", (recipe['id'], ingredient))
    conn.commit()
    
def get_stored_recipes(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT recipe_id, title FROM recipes")
    return cursor.fetchall()

    
create_database()



