import requests
import db

API_KEY = '4ca9539291f24558895a256986aadede'
FIND_BY_INGREDIENTS_URL = 'https://api.spoonacular.com/recipes/findByIngredients'


def get_recipes(ingredients):
    params = {
        'ingredients': ','.join(ingredients),
        'number': 5,
        'ranking': 1,
        'apiKey': API_KEY
    }
    response = requests.get(FIND_BY_INGREDIENTS_URL, params=params)
    recipes = response.json()
    
    detailed_recipes = []
    for recipe in recipes:
        title = recipe['title']
        url = f"https://spoonacular.com/recipes/{recipe['title'].replace(' ', '-').lower()}-{recipe['id']}"
        used_ingredients = [ing['name'] for ing in recipe.get('usedIngredients', [])]
        missed_ingredients = [ing['name'] for ing in recipe.get('missedIngredients', [])]
        detailed_recipes.append({
            'title': title,
            'url': url,
            'used_ingredients': used_ingredients,
            'missed_ingredients': missed_ingredients
        })
        db_recipe_id = db.add_recipe(title, url)
        for ingredient in used_ingredients + missed_ingredients:
            ingredient_id = db.add_ingredient(ingredient)
            db.add_recipe_ingredient(db_recipe_id, ingredient_id)
    
    return detailed_recipes





