import streamlit as st
from rec import rec_sys
from create_recipe import generate_recipes

st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://img.freepik.com/premium-photo/colorful-various-herbs-spices-cooking-dark-background_370312-476.jpg");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

st.markdown("# *Pantry Matchmaker :knife_fork_plate:*")

ingredients = st.text_input("Enter the ingredients you have (separated by commas)")

difficulty = st.selectbox('Choose a level of difficulty', ['Any','Super easy','Not too tricky','Showing off'])

st.markdown('Select any dietary preferences')

col1, col2, col3, col4 = st.columns([1,1,1,1])
glutenfree = col1.checkbox('Gluten-Free')
dairyfree = col2.checkbox('Dairy-Free')
vegetarian = col3.checkbox('Vegetarian')
vegan = col4.checkbox('Vegan')

diet = []
if glutenfree:
    diet.append('glutenfree')
if dairyfree:
    diet.append('dairyfree')
if vegetarian:
    diet.append('vegetarian')
if vegan:
    diet.append('vegan')

num = st.selectbox('How many recipes should be recommended?',[i for i in range(1,11)])

col5, col6, col7 = st.columns([1.25, 1, 0.05])

search = col5.button('Search for Recipes!')

generate = col6.button('Experiment with a newly created recipe!')

if search:
    recs = rec_sys(ingredients,difficulty,diet,num)
    recs = recs[['recipe_name','serves','cooking_time','ingredients','url']]
    recs['url'] = recs.apply(lambda x:f'<a target="_blank" href="{x["url"]}">Click Here</a>',axis=1)
    recs = recs.rename(columns={'recipe_name':'Recipe','serves':'Servings','cooking_time':'Approx. Time','ingredients':'Ingredients','url':'Full Recipe'})
    
    recs_html = recs.to_html(escape=False)
    recs_html = recs_html.replace('<th>', '<th style="text-align: center;">')
    st.markdown(recs_html, unsafe_allow_html=True)

if generate:
    recipe = generate_recipes(ingredients, difficulty, diet)
    st.markdown(recipe)

tooltip_text = """
<div class="tooltip">
  <div class="info-icon">i</div>
  <span class="tooltiptext">NOTE: This recipe is AI generated and may not be completely accurate, please exercise precautions.</span>
</div>
"""

col7.markdown(
    tooltip_text,
    unsafe_allow_html=True
)

st.write("""
    <style>
        .tooltip {
            position: relative;
            display: inline-block;
            cursor: pointer;
        }

        .info-icon {
            background-color: #000;
            color: #fff;
            border-radius: 50%;  /* Makes the background circular */
            width: 20px;  /* Width of the circle */
            height: 20px;  /* Height of the circle */
            text-align: center;
            line-height: 20px;  /* Vertically center the "i" inside the circle */
            font-weight: bold;  /* Make the "i" bold */
        }

        .tooltip .tooltiptext {
            visibility: hidden;
            width: 240px;
            background-color: #555;
            color: #fff;
            text-align: center;
            padding: 5px 0;
            border-radius: 6px;

            position: absolute;
            z-index: 1;
            bottom: 100%; 
            left: 50%;
            margin-left: -120px;
            
            opacity: 0;
            transition: opacity 0.3s;
        }

        .tooltip:hover .tooltiptext {
            visibility: visible;
            opacity: 1;
        }
    </style>
""", unsafe_allow_html=True)
