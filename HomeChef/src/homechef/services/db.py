import sqlite3
import pathlib
import json

_db = None

# --- DATABASE INITIALIZATION AND SCHEMA ---
def init_db():
    global _db
    if _db:
        return

    # Define the path to the database file in the project's root directory
    db_path = pathlib.Path(__file__).resolve().parent.parent.parent.parent / 'homechef.db'
    _db = sqlite3.connect(db_path)
    _db.row_factory = sqlite3.Row  # This allows accessing columns by name (e.g., row['title'])

    # Create the recipes table with the new 'image_path' column
    _db.execute('''
    CREATE TABLE IF NOT EXISTS recipes (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        ingredients TEXT,
        steps TEXT,
        time_minutes INTEGER,
        difficulty TEXT,
        image_path TEXT 
    )
    ''')
    # Create other necessary tables
    _db.execute('CREATE TABLE IF NOT EXISTS pantry (item TEXT PRIMARY KEY)')
    _db.execute('CREATE TABLE IF NOT EXISTS grocery (item TEXT PRIMARY KEY)')
    _db.commit()
    print("Database initialized successfully.")

# --- RECIPE FUNCTIONS ---
def add_recipe(recipe: dict):
    # This function now correctly handles the 'image_path' key
    ingredients_json = json.dumps(recipe.get('ingredients', []))
    steps_json = json.dumps(recipe.get('steps', []))
    
    _db.execute(
        '''
        INSERT OR REPLACE INTO recipes (id, title, ingredients, steps, time_minutes, difficulty, image_path)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''',
        (
            recipe['id'],
            recipe['title'],
            ingredients_json,
            steps_json,
            recipe.get('time_minutes'),
            recipe.get('difficulty'),
            recipe.get('image_path')  # Add the image path here
        )
    )
    _db.commit()

def get_recipes(query: str = None):
    cursor = _db.cursor()
    if query:
        cursor.execute("SELECT * FROM recipes WHERE title LIKE ?", ('%' + query + '%',))
    else:
        cursor.execute("SELECT * FROM recipes")
    
    recipes = []
    for row in cursor.fetchall():
        # Convert the row object to a dictionary
        recipe_dict = dict(row)
        # Decode the JSON strings back into Python lists
        recipe_dict['ingredients'] = json.loads(recipe_dict['ingredients'])
        recipe_dict['steps'] = json.loads(recipe_dict['steps'])
        recipes.append(recipe_dict)
    return recipes

# --- PANTRY FUNCTIONS ---
def get_pantry():
    return [row['item'] for row in _db.execute("SELECT item FROM pantry ORDER BY item")]

def set_pantry(items: list):
    _db.execute("DELETE FROM pantry")
    _db.executemany("INSERT OR IGNORE INTO pantry (item) VALUES (?)", [(i,) for i in items])
    _db.commit()

# --- GROCERY FUNCTIONS ---
def get_grocery():
    return [row['item'] for row in _db.execute("SELECT item FROM grocery ORDER BY item")]

def set_grocery(items: list):
    _db.execute("DELETE FROM grocery")
    if items:
        _db.executemany("INSERT OR IGNORE INTO grocery (item) VALUES (?)", [(i,) for i in items])
    _db.commit()

def add_grocery_item(item: str):
    _db.execute("INSERT OR IGNORE INTO grocery (item) VALUES (?)", (item,))
    _db.commit()

def remove_grocery_item(item: str):
    _db.execute("DELETE FROM grocery WHERE item=?", (item,))
    _db.commit()