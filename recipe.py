import requests
import db
import os

API_KEY = os.getenv('API_KEY')
SEARCH_URL = 'https://api.spoonacular.com/recipes/complexSearch'
RECIPE_INFO_URL = 'https://api.spoonacular.com/recipes/{id}/information'

# Get recipes from Spoonacular API based on input
# Input: list of ingredients
# Output: list of 5 recipes matching ingredients
def get_recipes(ingredients):
    recipes = []
    for ingredient in ingredients:
        params = {
            'includeIngredients': ingredient,
            'number': 5,  # Number of recipes to fetch
            'addRecipeInformation': True,  # Include detailed recipe information
            'includeNutrition': True,  # Ensure nutrition data is included
            'apiKey': API_KEY
        }
        response = requests.get(SEARCH_URL, params=params)
        data = response.json().get('results', [])

        for recipe in data:
            if 'id' in recipe:
                recipe_id = recipe['id']
                detailed_info = get_recipe_info(recipe_id)
                if detailed_info:
                    # Extract relevant recipe details
                    title = detailed_info.get('title', '')
                    url = detailed_info.get('sourceUrl', '')
                    nutrition_info = detailed_info.get('nutrition', {})  # Extract nutrition info

                    # Save recipe to database
                    db_recipe_id = db.add_recipe(title, url)

                    # Save ingredients to database
                    for ingred in detailed_info.get('extendedIngredients', []):
                        ingredient_name = ingred.get('name', '')
                        ingredient_id = db.add_ingredient(ingredient_name)
                        db.add_recipe_ingred(db_recipe_id, ingredient_id)

                    # Save nutrition information to database
                    if nutrition_info:
                        db.save_nutrition_info(db_recipe_id, nutrition_info)

                    recipes.append({
                        'title': title,
                        'url': url,
                        'ingredients': [ingred.get('name', '') for ingred in detailed_info.get('extendedIngredients', [])]
                    })

    return recipes

# Get recipe information from Spoonacular API
# Input: id of recipe
# Output: detailed information about the recipe
def get_recipe_info(recipe_id):
    url = RECIPE_INFO_URL.format(id=recipe_id)
    params = {
        'includeNutrition': True,  # Ensure nutrition data is included
        'apiKey': API_KEY
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch recipe info for recipe ID {recipe_id}. Status code: {response.status_code}")
        return None