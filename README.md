# Recipe Recommendation System

A web app that suggests recipes based on available ingredients,
helping to reduce food waste and simplify meal planning.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Technologies Used](#technologies-used)

## Overview

Many people struggle with deciding what to cook with the
ingredients they have on hand. The Recipe Recommendation System
provides recipe suggestions based on the ingredients available,
helping users reduce food waste and make meal planning easier.

## Features

- Enter ingredients to find recipes
- Save ingredients to a database
- Fetch recipes from the Spoonacular API
- Display top 5 recipe suggestions with links to the full recipes
- History Page that includes all ingredidents
- Extensive Nutrition Page

## Installation

### Prerequisites

- Python 3.6 or higher
- Pip (Python package installer)
- Spoonacular API key

### Steps

1. Clone the repository:
    ```bash
    git clone https://github.com/YOUR_USERNAME/recipe-recommendation-system.git
    cd recipe-recommendation-system
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up your Spoonacular API key in `recipe.py`:
    ```python
    API_KEY = 'YOUR_SPOONACULAR_API_KEY'
    ```

5. Initialize the database:
    ```bash
    python app.py
    ```

## Usage

1. Run the Flask application:
    ```bash
    python app.py
    ```

2. Open your web browser and go to `http://127.0.0.1:5000/`.

3. Enter your ingredients in the provided form and click
"Find Recipes".

4. View the recipe suggestions and click on the links to see
the full recipes.

## Technologies Used

- Python
- Flask
- SQLite
- Spoonacular API
- HTML/CSS

