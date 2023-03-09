import streamlit as st
from PIL import Image

# Configuration
st.set_page_config(page_title='What does the data tell us?', page_icon=':bar_chart:', layout='wide')

# Title
st.header('What does the data 📈📊📉 tell us?')

# Content
st.subheader("What is the propotion of fresh vegetable produce sold by weight vs. by piece?")
# # (static) plot 1
image = Image.open('ratio_of_fresh_vegetable_produce_sold_by_ct_vs_weight.png')
st.image(image, width=500)

# 
st.subheader("How does the price distribution look like in the two groups?")
# # (static) plot 2
image = Image.open('distribution_of_lowest_prices_per_lb.png')
st.image(image, width=500)
# 
