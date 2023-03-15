import streamlit as st
from PIL import Image

# Configuration
st.set_page_config(page_title='CABAM (Create A Balanced, Affordable Meal)', page_icon=':bar_chart:', layout='wide')

# Title
st.title('CABAM (Create A Balanced, Affordable Meal)')
st.write(
    """
    Created by Vanessa Kan
    """
)

# Content
st.header("Objective")
st.write(
    """
    CABAM helps users plan their grocery shopping (especially with fresh produce) by searching for and comparing recipes with the best nutrition value.
    """
)
# 
st.header("How does it work?")
st.write(
    """
    Based on the user's ZIPCODE, CABAM searches for the closest Kroger store location and retrieves a list of vegetable products available at that location. 
    Users can choose their priority: food or budget? In either case, recipes with the best nutrition value are returned! 
    So what's the difference? Food -> top 3 cheapest vs. Budget -> cheapest fresh ingredient. 
    Using the ingredient, CABAM searches for relevant recipes from Edamam and calculates the nutrition score using the "Nutrition Score Pyramid" that is based on the recommended daily intake of each nutrient. 
    Users can then choose from the top 3 healthiest recipes and decide on serving size. 
    CABAM then extracts a list of ingredients using the ingredient-parser-nlp, determines the cheapest price and generates a grocery list for all the fresh produce needed for the recipe!
    """
)
image = Image.open('CABAM_flow chart_transparent_bkgd.png')
st.image(image, width=800)
st.write(
 """
 CABAM currently only supports vegetarian recipes and vegetable products from Kroger grocery stores, and you can test the app with ZIPCODE "75204"
 """
)
# 
st.header("What is the 'Nutrition Score Pyramid?'")
st.write(
    """
    The Nutrition Score Pyramid is developed based on the recommended daily intake (RDI) of nutrients. 
    If there is no RDI or if that value exceeds 100% (too much of a good thing? 😉), then a negative score is assigned.
    For the remaining nutrients, a score is assigned incrementally.
    """
)
image = Image.open('CABAM_nutrition_score_pyramid_transparent_bkgd.png')
st.image(image, width=500)
# 
st.header("Future directions")
st.write("▶️ Expand to other fresh groceries")
st.write("▶️ Broaden the scope of grocery stores")
st.write("▶️ Implement a recommendation engine for recipes that uses the same/similar ingredients (That way, you know what to do with the leftover ingredients!)")
# 
st.header("Technologies used")
st.write(
    """
    Python, REST API, NLP, streamlit, pandas, Kroger APIs, Edamam API
    """
)