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

#Save a list of ingredients to database
def get_ingredients():
    conn = sqlite3.connect('ingredients.db')
    c = conn.cursor()
    c.execute('SELECT name FROM ingredients')
    ingredients = [row[0] for row in c.fetchall()]
    conn.close()
    return ingredients

#Intialize database 
create_database()



