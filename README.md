# CABAM (Create A Balanced, Affordable Meal)

### Objective
CABAM helps users plan their grocery shopping (especially with fresh produce) by searching for and comparing recipes with the best nutrition value. 

### How does it work?
Based on the user's ZIPCODE, CABAM searches for the closest Kroger store location and retrieves a list of vegetable products available at that location. Users can choose their priority: food or budget? In either case, recipes with the best nutrition value are returned! So what's the difference? Food -> top 3 cheapest vs. Budget -> cheapest fresh ingredient. Using the ingredient, CABAM searches for relevant recipes from Edamam and calculates the nutrition score using the "Nutrition Score Pyramid" that is based on the recommended daily intake of each nutrient. Users can then choose from the top 3 healthiest recipes and decide on serving size. CABAM then extracts a list of ingredients using the [ingredient-parser-nlp](https://pypi.org/project/ingredient-parser-nlp/), determines the cheapest price and generates a grocery list for all the fresh produce needed for the recipe!

<img src="https://github.com/kwyvanessa/CABAM/blob/main/CABAM_flow%20chart_transparent_bkgd.png" width="750" height="500">

CABAM currently only supports vegetarian recipes and vegetable products from Kroger grocery stores, and you can test the app with ZIPCODE "75204"

### What is the "Nutrition Score Pyramid"?
<img src="https://github.com/kwyvanessa/CABAM/blob/main/CABAM_nutrition_score_pyramid_transparent_bkgd.png" width="550" height="350">

### How do you access it?
At the moment, you can access CABAM using https://kwyvanessa-cabam.streamlit.app/

### Future directions
* Expand to other fresh groceries
* Broaden the scope of grocery stores 
* Implement a recommendation engine for recipes that uses the same/similar ingredients (That way, you know what to do with the leftover ingredients!)

Technologies used: Python, REST API, NLP, streamlit, pandas, [Kroger APIs](https://developer.kroger.com/), [Edamam API](https://www.edamam.com/)
