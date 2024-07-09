import sqlite3

def create_database():
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

    c.execute('''
        CREATE TABLE IF NOT EXISTS nutrient_info (
            name TEXT,
            amount REAL,
            unit TEXT,
            percentOfDailyNeeds REAL,
            ingredient_id INTEGER,
            FOREIGN KEY (ingredient_id) REFERENCES ingredients(id),
            UNIQUE (ingredient_id)
        )
    ''')
    conn.commit()
    conn.close()

#Add one ingredient to ingredients table or retrieve ID if it exists
def add_ingredient(name):
    conn = sqlite3.connect('recipes.db')
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO ingredients (name) VALUES (?)', (name,))
    c.execute('SELECT id FROM ingredients WHERE name = ?', (name,))
    ingredient_id = c.fetchone()[0]
    conn.commit()
    conn.close()
    return ingredient_id

#Add one recipe to recipes table or retrieve ID if it exists
def add_recipe(title, url):
    conn = sqlite3.connect('recipes.db')
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO recipes (title, url) VALUES (?, ?)', (title, url))
    c.execute('SELECT id FROM recipes WHERE title = ? AND url = ?', (title, url))
    recipe_id = c.fetchone()[0]
    conn.commit()
    conn.close()
    return recipe_id

#Associate an ingredient with a recipe in the recipe_ingredients table
def add_recipe_ingred(recipe_id, ingredient_id):
    conn = sqlite3.connect('recipes.db')
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO recipe_ingredients (recipe_id, ingredient_id) VALUES (?, ?)', (recipe_id, ingredient_id))
    conn.commit()
    conn.close()

#Get all ingredients from the ingredients table
def get_ingredients():
    conn = sqlite3.connect('recipes.db')
    c = conn.cursor()
    c.execute('SELECT DISTINCT name FROM ingredients')
    ingredients = [row[0] for row in c.fetchall()]
    conn.close()
    return ingredients

#Get all recipes along with their associated ingredients
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


def add_nutrient_info(name, amount, unit, percent_of_daily_needs, ingredient_id):
    conn = sqlite3.connect('recipes.db')
    c = conn.cursor()
    
    c.execute('''
        INSERT INTO nutrient_info (name, amount, unit, percentOfDailyNeeds, ingredient_id)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, amount, unit, percent_of_daily_needs, ingredient_id))
    
    conn.commit()
    conn.close()


def get_ingredients_with_nutrients():
    conn = sqlite3.connect('recipes.db')
    c = conn.cursor()
    
    c.execute('''
        SELECT ingredients.name, nutrient_info.name, nutrient_info.amount, nutrient_info.unit, nutrient_info.percentOfDailyNeeds
        FROM ingredients
        LEFT JOIN nutrient_info ON ingredients.id = nutrient_info.ingredient_id
    ''')
    
    ingredients = []
    for row in c.fetchall():
        ingredients.append({
            'ingredient_name': row[0],
            'nutrient_name': row[1],
            'amount': row[2],
            'unit': row[3],
            'percent_of_daily_needs': row[4]
        })
    
    conn.close()
    return ingredients


#Clear all data from the database
def clear_database():
    conn = sqlite3.connect('recipes.db')
    c = conn.cursor()
    c.execute('DELETE FROM recipe_ingredients')
    c.execute('DELETE FROM recipes')
    c.execute('DELETE FROM ingredients')
    conn.commit()
    conn.close()

# Initialize the database by creating the tables.
create_database()
