import streamlit as st
import google.generativeai as genai
from secret_key import openapi_key

# Step 1: Configure Gemini API key
genai.configure(api_key=openapi_key) # 🔁 Repplace with your actual Gemini API key

# Step 2: Load the model
model = genai.GenerativeModel("models/gemini-2.5-flash")

# Step 3: Streamlit UI
st.set_page_config(page_title="🍽️ Restaurant Menu Generator", layout="centered")
st.title("🍽️ Fancy Restaurant Name & Menu Generator")

# Step 4: Get user input
cuisine = st.text_input("Enter a cuisine (e.g., Italian, Indian, Chinese):", "")

if st.button("Generate") and cuisine:
    with st.spinner("Cooking...🧑🏻‍🍳"):

        # Generate restaurant name
        prompt_name = f"Suggest a single fancy and unique name for a {cuisine} restaurant. Only give the name, no explanation."
        name_response = model.generate_content(prompt_name)
        restaurant_name = name_response.text.strip()

        # Generate ordered menu
        prompt_menu = (
            f"Suggest 6 unique and creative menu items for a restaurant named '{restaurant_name}', "
            f"serving {cuisine} cuisine. Return the menu items as a numbered list (1. ..., 2. ..., etc.)."
        )
        menu_response = model.generate_content(prompt_menu)
        menu_raw = menu_response.text.strip()

        # Post-processing (cleaning if needed)
        menu_items = []
        for line in menu_raw.splitlines():
            if line.strip() and line.strip()[0].isdigit():
                # Remove number prefix and clean
                item = line.split('.', 1)[-1].strip()
                menu_items.append(item)

    # Output
    st.subheader("🏪 Restaurant Name")
    st.success(restaurant_name)

    st.subheader("🍽️ Menu Items")
    for i, item in enumerate(menu_items, 1):
        st.markdown(f"**{i}. {item}**")
