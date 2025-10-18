import json, pathlib
from .services import db

def main():
    db.init_db()
    
    # Check if recipes with images already exist to prevent duplicates
    recipes_with_images = [r for r in db.get_recipes() if r.get('image_url')]
    if recipes_with_images:
        print("Database already contains recipes with image URLs. Skipping seeding.")
        return

    data_path = pathlib.Path(__file__).resolve().parents[1] / 'homechef' / 'data' / 'recipes.json'
    recipes = json.loads(data_path.read_text(encoding='utf-8'))
    inserted = 0
    for r in recipes:
        db.add_recipe(r)
        inserted += 1
    print(f"Inserted {inserted} recipes into the database.")

if __name__ == '__main__':
    main()
