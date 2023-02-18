import streamlit as st
import time
from PIL import Image
from location import extract_location_info, extract_store_location_id
from vegetable_products import extract_vegetable_products, extract_cheapest_vegetable_products
from recipe import calculate_nutrition_score_for_each_recipe
from ingredients import get_recipe_url
from grocery_list import get_grocery_list

st.markdown("""
<style>
.subheader-font {
    font-size:30px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.question-font {
    font-size:20px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.instruction-font {
    font-size:15px;
}
</style>
""", unsafe_allow_html=True)

image = Image.open('CABAM_logo.png')
st.image(image, width=680)
st.title("Create A Balanced Affordable Meal")
st.markdown('<p class="subheader-font">Let us know... 🤔.</p>', unsafe_allow_html=True)

priority = ''

st.markdown('<p class="question-font">Where you are located 📍.</p>', unsafe_allow_html=True)
location = st.number_input('Enter your ZIPCODE',
    min_value = 00000, max_value = 99999)
st.write('You entered ', location)

if location != 0:
    st.text(extract_location_info(location))
    location_id = extract_store_location_id(location)
    st.text("")
    st.markdown('<p class="question-font">What is more important to you ☝️</p>', unsafe_allow_html=True)
    priority = st.selectbox(
        'Your priority.',
        ('Nutritious food ⚖️','Budget 🏦','Meh 🤷‍♀️🤷🤷‍♂️ can you decide for me?'))
        # default: nutritious food
    st.write('You selected:', priority)    

    st.text("")
    st.markdown('<p class="question-font">Which of the following you would like to see on your plate 🍽</p>', unsafe_allow_html=True)
    if priority == 'Budget 🏦':
        vegetable_list = extract_cheapest_vegetable_products(location_id)
        ingredient = st.selectbox(
            'Pick an ingredient!',
            (vegetable_list))
    else:
        vegetable_list = extract_vegetable_products(location_id)
        vegetable_list.insert(0, 'none')
        ingredient = st.selectbox(
            'Pick an ingredient!',
            (vegetable_list))
        st.write('You selected:', ingredient)

    if ingredient != 'none':
        st.text("")
        recipes = calculate_nutrition_score_for_each_recipe(ingredient)
        recipes_list = recipes['recipe_name'].tolist()[0:3]
        recipes_list.insert(0, 'none')
        selected_recipe = st.selectbox(
            'Pick your dish.',
            (recipes_list))
        if selected_recipe != 'none':
            recipe_idx = recipes.index[recipes['recipe_name'] == selected_recipe].tolist()[0]

        portion = 0
        if selected_recipe != 'none':
            st.text("")
            st.markdown('<p class="question-font">How many servings 🍽 would you like?</p>', unsafe_allow_html=True)
            portion = st.number_input('Enter # of servings',
                min_value = 0, max_value = 99999)
            st.write('You selected:', portion, 'servings')            
    
        if portion != 0:
            st.text("")
            st.markdown('<p class="subheader-font">Just sit back and relax while we plan your next grocery trip... 🧘‍♀️🧘🧘‍♂️</p>', unsafe_allow_html=True)
            st.text("")
            st.write('Here is a link to the recipe 🔗:', get_recipe_url(ingredient, recipe_idx))
            st.text("")
            st.download_button(
                "⬇️ Download your grocery list",
                data = get_grocery_list(location_id, ingredient, recipe_idx, portion).to_csv() ,
                file_name = 'grocery_list.csv',
                mime='text/csv'
             )
