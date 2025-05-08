# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col,when_matched

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
  """Choose th fruit you want in your custom smoothie
  """
)

# Get the current credentials
session = get_active_session()

order_name = st.text_input("Order name", "Life of Brian")
st.write("The current movie title is", order_name)

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    "Choose upto 5 ingredients?",
    my_dataframe,
    max_selections=5
)

if ingredients_list:

    ingredients_string = ''

    for each_fruit in ingredients_list:
        ingredients_string += each_fruit + ' '
    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + order_name + """')"""
    
    insert_order = st.button('Submit Order')

    if insert_order:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered ' + order_name + '!', icon="✅")
