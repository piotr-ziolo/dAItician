import streamlit as st
from utils import create_meals, get_ingredient_categories

def display_sidebar():
    st.sidebar.image('images/ai_cook.png', use_column_width=True)
    st.sidebar.title('dAItician')
    st.sidebar.markdown("### About")
    st.sidebar.info(
        """
        **dAItician** helps you create a personalized meal plan based on the ingredients you have at home. 
        Simply select your preferences and ingredients, and click 'Generate' to see your AI-powered customized meal plan.
        """
    )
    st.sidebar.markdown("### Instructions")
    st.sidebar.write(
        """
        1. Select your daily calorie limit.
        2. Choose the number of meals.
        3. Pick the ingredients you have.
        4. Click 'Generate' to create your meal plan.
        """
    )

def main():
    st.set_page_config(page_title="DAItician", page_icon="images/ai_cook.png", initial_sidebar_state='collapsed')
    display_sidebar()
    
    col1, col2 = st.columns([0.9, 0.1])
    with col1:
        st.markdown('# Welcome to dAItician!')
    with col2:
        st.image('images/ai_cook.png', width=80)
    
    st.write("To get started, use the tabs below to select your preferences and ingredients, then click 'Generate' to see your personalized meal plan.")

    tab1, tab2, tab3 = st.tabs(["Calorie Limit", "Number of Meals", "Ingredients"])

    with tab1:
        st.subheader('Select the daily calorie limit:')
        kcal = st.slider('Kcal', 1000, 3500, 2000, 100, format='%d kcal', label_visibility='visible')

    with tab2:
        st.subheader('Select the number of meals:')
        no_of_meals = st.slider('Number of meals', 3, 6, 5, 1, label_visibility='visible')

    with tab3:
        st.subheader('Select ingredients:')
        ingredient_categories = get_ingredient_categories()
        selected_ingredients = []
        for category, items in ingredient_categories.items():
            selected_items = st.multiselect(f'Select {category.lower()}:', items)
            selected_ingredients.extend(selected_items)

        others_selected = st.text_input('Other ingredients (comma-separated):', value='', help="Enter any other ingredients not listed above.")
        if others_selected:
            selected_ingredients.extend(map(str.strip, others_selected.split(',')))

    is_ingredient_selected = bool(selected_ingredients)
    
    # Generate button container with message
    generate_button = st.button(label='Generate', disabled=not is_ingredient_selected, type='primary')
    
    if not is_ingredient_selected:
        st.warning("Please select at least one ingredient to generate the meal plan.")

    if generate_button and is_ingredient_selected:
        try:
            with st.spinner('Generating your meal plan...'):
                response = create_meals(selected_ingredients, kcal, no_of_meals)
            if response:
                st.subheader('Your meal plan:')
                with st.expander("View meal plan details", expanded=True):
                    st.write(response)

                meal_plan_file = response.encode('utf-8')
                st.download_button(label='Save the meal plan', data=meal_plan_file, file_name='meal_plan.txt', mime='text/plain')
        except RuntimeError as e:
            st.error(str(e))

    # Footer
    st.markdown("""
        <div style='text-align: center; color: #666; margin-top: 80px; padding-top: 20px; border-top: 1px solid #eaeaea;'>
            <p>Created by Piotr Ziolo ( <a href="https://www.linkedin.com/in/piotr-ziolo/" target="_blank">LinkedIn</a> | <a href="https://github.com/piotr-ziolo" target="_blank">GitHub</a> )</p>
            <p>Inspired by Andrei Dumitrescu's <a href="https://udemy.com/course/openai-api-chatgpt-gpt4-with-python-bootcamp/" target="_blank">OpenAI API with Python Bootcamp: ChatGPT API, GPT-4, DALL·E</a></p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
