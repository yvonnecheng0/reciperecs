import unittest
import db

class TestDatabaseOperations(unittest.TestCase):

    def test_add_ingredient(self):
        #Test adding an ingredient to the database
        ingredient_id = db.add_ingredient("Tomato")
        self.assertIsInstance(ingredient_id, int)

        ingredients = db.get_ingredients()
        self.assertIn("Tomato", ingredients)

    def test_add_duplicate_ingredient(self):
        #Test adding a duplicate ingredient to the database
        ingredient_id1 = db.add_ingredient("Tomato")
        ingredient_id2 = db.add_ingredient("Tomato")
        self.assertEqual(ingredient_id1, ingredient_id2)

        ingredients = db.get_ingredients()
        self.assertEqual(ingredients.count("Tomato"), 1)


    def test_add_recipe_with_ingredients(self):
        #Test adding a recipe with ingredients to the database
        recipe_id = db.add_recipe("Tomato Soup", "http://example.com/tomato-soup")
        ingredient_id1 = db.add_ingredient("Tomato")
        ingredient_id2 = db.add_ingredient("Basil")
        db.add_recipe_ingredient(recipe_id, ingredient_id1)
        db.add_recipe_ingredient(recipe_id, ingredient_id2)

        recipes = db.get_recipes_with_ingredients()
        self.assertEqual(len(recipes), 1)
        self.assertEqual(recipes[0]['title'], "Tomato Soup")
        self.assertEqual(set(recipes[0]['ingredients']), {"Tomato", "Basil"})

    def test_clear_database(self):
        #Test clearing the database
        db.add_recipe("Tomato Soup", "http://example.com/tomato-soup")
        db.add_ingredient("Tomato")
        db.clear_database()

        recipes = db.get_recipes_with_ingredients()
        ingredients = db.get_ingredients()
        self.assertEqual(len(recipes), 0)
        self.assertEqual(len(ingredients), 0)

if __name__ == '__main__':
    unittest.main()



