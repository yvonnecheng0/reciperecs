import requests
import db
import os

API_KEY = '0f1dd104f432475e954460260406090e'
SEARCH_URL = 'https://api.spoonacular.com/recipes/complexSearch'
RECIPE_INFO_URL = 'https://api.spoonacular.com/recipes/{id}/information'
FIND_BY_INGREDIENTS_URL = 'https://api.spoonacular.com/recipes/findByIngredients'
# Get recipes from Spoonacular API based on input
# Input: list of ingredients
# Output: list of 5 recipes matching ingredients


'''Currently trying to integrate the function for missing and used 
ingredidents as well as my function for the nutrition page'''

def get_recipes(ingredients, detailed_search=True):
    recipes = []
    if detailed_search:
        for ingredient in ingredients:
            params = {
                'includeIngredients': ingredient,
                'number': 5,  # Number of recipes to fetch
                'ranking': 1,
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
                        save_recipe_to_database(detailed_info)
                        recipes.append(format_recipe_data(detailed_info))
    else:
        detailed_recipes = []  # Initialize the list before using it
        params = {
            'ingredients': ','.join(ingredients),
            'number': 5,
            'ranking': 1,
            'apiKey': API_KEY
        }
        response = requests.get(FIND_BY_INGREDIENTS_URL, params=params)
        recipes = response.json()

        for recipe in recipes:
            detailed_recipes.append(save_and_format_by_ingredient(recipe))

    return detailed_recipes if not detailed_search else recipes

def get_recipe_info(recipe_id):
    url = RECIPE_INFO_URL.format(id=recipe_id)
    params = {
        'includeNutrition': True,  # Ensure nutrition data is included
        'apiKey': API_KEY
    }
    response = requests.get(url, params=params)
    return response.json() if response.status_code == 200 else None

def save_recipe_to_database(recipe):
    db_recipe_id = db.add_recipe(recipe['title'], recipe['sourceUrl'])
    for ingred in recipe.get('extendedIngredients', []):
        ingredient_id = db.add_ingredient(ingred['name'])
        db.add_recipe_ingred(db_recipe_id, ingredient_id)
    if recipe.get('nutrition'):
        db.save_nutrition_info(db_recipe_id, recipe['nutrition'])

def format_recipe_data(recipe):
    return {
        'title': recipe.get('title', ''),
        'url': recipe.get('sourceUrl', ''),
        'ingredients': [ing['name'] for ing in recipe.get('extendedIngredients', [])]
    }

def save_and_format_by_ingredient(recipe):
    title = recipe['title']
    url = f"https://spoonacular.com/recipes/{title.replace(' ', '-').lower()}-{recipe['id']}"
    db_recipe_id = db.add_recipe(title, url)
    used_ingredients = [ing['name'] for ing in recipe.get('usedIngredients', [])]
    missed_ingredients = [ing['name'] for ing in recipe.get('missedIngredients', [])]
    for ingredient in used_ingredients + missed_ingredients:
        ingredient_id = db.add_ingredient(ingredient)
        db.add_recipe_ingred(db_recipe_id, ingredient_id)
    return {
        'title': title,
        'url': url,
        'used_ingredients': used_ingredients,
        'missed_ingredients': missed_ingredients
    }

'''def get_recipes(ingredients):
    recipes = []
    for ingredient in ingredients:
        params = {
            'includeIngredients': ingredient,
            'number': 5,  # Number of recipes to fetch
            'ranking':1,
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

def new_get_recipes(ingredients):
    params = {
        'ingredients': ','.join(ingredients),
        'number': 5,
        'ranking': 1,
        'apiKey': API_KEY
    }
    response = requests.get(FIND_BY_INGREDIENTS_URL, params=params)
    if response.status_code != 200:
        print("Error fetching recipes:", response.text)
        return []  # Return empty list or handle error as needed

    recipes = response.json()

    detailed_recipes = []
    for recipe in recipes:
        if 'title' not in recipe or 'id' not in recipe:
            print("Missing required data in recipe:", recipe)
            continue  # Skip this recipe

        title = recipe['title']
        url = f"https://spoonacular.com/recipes/{title.replace(' ', '-').lower()}-{recipe['id']}"
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
            db.add_recipe_ingred(db_recipe_id, ingredient_id)

    return detailed_recipes'''
