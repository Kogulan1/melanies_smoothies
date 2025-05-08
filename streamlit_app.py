# Import python packages
import streamlit as st
import pandas as pd
from snowflake.snowpark.functions import col,when_matched
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
  """Choose th fruit you want in your custom smoothie
  """
)

# Get the current credentials
cnx = st.connection("snowflake")
session = cnx.session()



order_name = st.text_input("Order name", "Life of Brian")
st.write("The current movie title is", order_name)

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col("SEARCH_ON"))
pd_df = my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()

ingredients_list = st.multiselect(
    "Choose upto 5 ingredients?",
    my_dataframe,
    max_selections=5
)

if ingredients_list:

    ingredients_string = ''

    for each_fruit in ingredients_list:
      ingredients_string += each_fruit + ' '

      search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
      st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
      
      st.subheader(each_fruit + 'Nutrition Information')
      smoothiefroot_respone = requests.get("https://my.smoothiefroot.com/api/fruit/" + each_fruit)
      sf_df = st.dataframe(smoothiefroot_respone.json(), use_container_width = True)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + order_name + """')"""
    
    insert_order = st.button('Submit Order')

    if insert_order:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered ' + order_name + '!', icon="✅")



