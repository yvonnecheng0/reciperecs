import requests
import db

API_KEY = 'ab4412b72bb448f28ac243f5210c8e84'
SEARCH_URL = 'https://api.spoonacular.com/recipes/complexSearch'
RECIPE_INFO_URL = 'https://api.spoonacular.com/recipes/{id}/information'

# Get recipes from Spoonacular API based on input
# Input: list of ingredients
# Output: list of 5 recipes matching ingredients


def get_recipes(ingredients):
    params = {
        'includeIngredients': ','.join(ingredients),
        'number': 5,
        'addRecipeInformation': True,
        'apiKey': API_KEY
    }
    response = requests.get(SEARCH_URL, params=params)
    recipes = response.json().get('results', [])

    for recipe in recipes:
        if 'id' in recipe:
            recipe_id = recipe['id']
            detailed_info = get_recipe_info(recipe_id)
            if detailed_info:
                title = detailed_info['title']
                url = detailed_info['sourceUrl']
                db_recipe_id = db.add_recipe(title, url)
                for ingredient in ingredients:
                    ingredient_id = db.add_ingredient(ingredient)
                    db.add_recipe_ingred(db_recipe_id, ingredient_id)

    return recipes

# Get recipe information from Spoonacular API
# Input: id of recipe
# Output is detailed information about the recipe


def get_recipe_info(recipe_id):
    url = RECIPE_INFO_URL.format(id=recipe_id)
    params = {
        'apiKey': API_KEY
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    return None
