import streamlit as st
import requests

# Replace 'YOUR_APP_ID' and 'YOUR_API_KEY' with your actual Edamam API credentials
APP_ID = '6caff4e6'
API_KEY = '8b9a7c2ed9ad88d54e8ae13b88bbf7a3'

# Base URL for the Edamam Recipe Search API
BASE_URL = 'https://api.edamam.com/search'

# Function to fetch recipes based on user input
def fetch_recipes(ingredient, from_index=0):
    params = {
        'q': ingredient,  
        'app_id': APP_ID,
        'app_key': API_KEY,
        'from': from_index,
        'to': from_index + 10
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        return data['hits']
    else:
        return None

# Function to display recipe details
def display_recipe_details(recipe):
    st.subheader(recipe['recipe']['label'])
    st.image(recipe['recipe']['image'])
    st.write("Ingredients:")
    for ingredient in recipe['recipe']['ingredients']:
        st.write(f"- {ingredient['text']}")
    st.write("Calories:", round(recipe['recipe']['calories']))
    st.write("Cooking Time:", recipe['recipe']['totalTime'])
    st.write("Nutritional Value:")
    for nutrient in recipe['recipe']['digest']:
        st.write(f"- {nutrient['label']}: {round(nutrient['total'], 2)} {nutrient['unit']}")

# Main function to run the Streamlit app
def main():
    st.title("Recipe Generator")

    ingredient = st.text_input("Enter an ingredient:", "chicken")
    recipes = None  # Initialize recipes variable

    if st.button("Search", key="search_button"):
        recipes = fetch_recipes(ingredient)
        if recipes:
            st.write(f"Top 10 {ingredient.capitalize()} Recipes:")
            for i, recipe in enumerate(recipes):
                st.write(f"{i+1}. {recipe['recipe']['label']}")
        else:
            st.error("Error fetching recipes. Please try again later.")

    from_index = 0
    while st.button("Load More Recipes", key="load_more_button"):
        from_index += 10
        recipes = fetch_recipes(ingredient, from_index)
        if not recipes:
            st.warning("No more recipes available.")
            break
        for i, recipe in enumerate(recipes):
            st.write(f"{i+from_index+1}. {recipe['recipe']['label']}")

    if recipes is not None:  # Check if recipes is not None before accessing it
        selected_recipe_index = st.number_input("Enter the number corresponding to the recipe you'd like to explore:", 1, from_index+10)
        if st.button("View Recipe", key="view_recipe_button"):
            selected_recipe = recipes[selected_recipe_index - 1 - from_index]
            display_recipe_details(selected_recipe)

        if st.button("View Cooking Method", key="view_cooking_method_button"):
            selected_recipe = recipes[selected_recipe_index - 1 - from_index]
            cooking_method_url = selected_recipe['recipe']['url']
            st.write("Click below to view the cooking method:")
            st.markdown(f"[View Cooking Method]({cooking_method_url})")

if __name__ == "__main__":
    main()