import os
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv(find_dotenv(), override=True)
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("The OPENAI_API_KEY environment variable is not set. Please set it in your .env file.")

client = OpenAI(api_key=api_key)

def create_meals(ingredients: list, kcal: int = 2000, no_of_meals: int = 5) -> str:
    """Create a daily meal plan based on ingredients, calorie limit, and number of meals."""
    prompt = f"""
    Create a healthy daily meal plan for {no_of_meals} meals,
    based on the following ingredients: {', '.join(ingredients)}.
    Do NOT use ingredients that are not listed.
    The total should be around {kcal} kcal.
    Assign a suggestive and concise title to each meal.
    Include the estimated number of calories next to the title of each meal.
    Make sure the title is formatted as follows: "### breakfast, lunch, etc.: Title (calories)".
    Explain how to prepare each recipe.
    Add extra empty lines in between each recipe in the following format: "\\n---\\n".
    """

    messages = [
        {'role': 'system', 'content': 'You are a talented cook & dietician, capable of designing healthy meal plans for a day.'},
        {'role': 'user', 'content': prompt},
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=1024,
            temperature=0.8,
            n=1
        )
        return response.choices[0].message.content
    except Exception as e:
        raise RuntimeError(f"An error occurred: {e}")

def get_ingredient_categories() -> dict:
    """Return a dictionary of ingredient categories and their items, sorted alphabetically."""
    categories = {
        'Vegetables': ['carrots', 'broccoli', 'spinach', 'kale', 'tomatoes', 'cucumbers', 'bell peppers', 'onions', 'garlic', 'ginger', 'potatoes', 'sweet potatoes', 'zucchini', 'mushrooms', 'lettuce', 'cabbage', 'cauliflower', 'asparagus', 'green beans', 'peas', 'corn', 'eggplant', 'beets', 'radishes', 'celery', 'squash', 'pumpkin', 'artichokes', 'leeks', 'fennel', 'turnips', 'rutabaga', 'parsnips', 'okra', 'brussels sprouts'],
        'Fruits': ['apples', 'bananas', 'oranges', 'grapes', 'strawberries', 'blueberries', 'raspberries', 'blackberries', 'kiwi', 'pineapple', 'mango', 'peaches', 'plums', 'cherries', 'watermelon', 'cantaloupe', 'honeydew', 'papaya', 'pomegranate', 'figs', 'dates', 'passion fruit', 'guava', 'lychee', 'dragon fruit', 'star fruit', 'persimmons', 'cranberries', 'apricots', 'tangerines', 'grapefruit', 'lemons', 'limes', 'coconut', 'avocado'],
        'Dairy': ['milk', 'yogurt', 'cheese', 'butter', 'cream', 'sour cream', 'cream cheese', 'cottage cheese', 'ricotta', 'mozzarella', 'cheddar', 'parmesan', 'feta', 'goat cheese', 'blue cheese', 'brie', 'camembert', 'gouda'],
        'Meat': ['beef', 'chicken', 'pork', 'lamb', 'turkey', 'duck', 'goose', 'quail', 'rabbit', 'venison', 'elk', 'bison', 'boar', 'ostrich', 'emu', 'kangaroo', 'alligator', 'snake', 'turtle', 'crab', 'lobster', 'shrimp', 'prawns', 'clams', 'mussels', 'scallops', 'octopus', 'squid', 'calamari', 'anchovies', 'sardines', 'mackerel', 'herring', 'trout', 'salmon', 'tuna', 'cod', 'halibut', 'sole', 'flounder', 'catfish'],
        'Grains': ['bread', 'rice', 'pasta', 'couscous', 'quinoa', 'bulgur', 'barley', 'oats', 'cornmeal', 'polenta', 'millet', 'farro', 'spelt', 'teff', 'amaranth', 'buckwheat', 'rye', 'wheat', 'sorghum', 'kamut', 'triticale', 'wild rice', 'brown rice', 'white rice', 'jasmine rice', 'basmati rice', 'arborio rice', 'sushi rice', 'short-grain rice', 'long-grain rice']
    }

    # Sort ingredients within each category alphabetically
    for category in categories:
        categories[category].sort()

    return categories
