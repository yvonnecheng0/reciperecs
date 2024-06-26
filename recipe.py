import requests

API_KEY = 'ab4412b72bb448f28ac243f5210c8e84'
API_URL = 'https://api.spoonacular.com/recipes/complexSearch'

#Get recipes from Spoonacular API based on input 
#Input: list of ingredients 
#Output: list of 5 recipes matching ingredients
def get_recipes(ingredients):
    params = {
        'includeIngredients': ','.join(ingredients),
        'number': 5,
        'addRecipeInformation': True,
        'apiKey': API_KEY
    }
    response = requests.get(API_URL, params=params)
    return response.json().get('results', [])
