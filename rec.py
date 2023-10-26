import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity  
from web_scraping_nlp.nlp import ingredient_parser
import pickle
import unidecode, ast
import numpy as np

def title_parser(title):
    title = unidecode.unidecode(title)
    return title 

def ingredient_parser_final(ingredient):
    if isinstance(ingredient, list):
        ingredients = ingredient
    else:
        ingredients = ast.literal_eval(ingredient)    
    ingredients = ','.join(ingredients)
    ingredients = unidecode.unidecode(ingredients)
    return ingredients

def get_recommendations(N, scores, diet, difficulty):
    df_recipes = pd.read_csv('input_data/parsed_ingreds_recipes.csv')
    top = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:5466]
    recommendation = pd.DataFrame(columns = ['recipe_name', 'serves', 'cooking_time', 'ingredients', 'url', 'score'])
    count = 0
    for i in top:
        if difficulty == "Any":
            pass
        elif df_recipes['difficulty'][i] != difficulty:
            continue
        try:
            counter=0
            for d in diet:
                if d not in eval(df_recipes['diet'][i]):
                    counter+=1
            if counter != 0:
                continue
        except:
            continue
        recommendation.at[count, 'recipe_name'] = title_parser(df_recipes['recipe_name'][i])
        recommendation.at[count, 'serves'] = df_recipes['serves'][i]
        recommendation.at[count, 'cooking_time'] = df_recipes['cooking_time'][i]
        recommendation.at[count, 'ingredients'] = ingredient_parser_final(df_recipes['ingredients'][i])
        recommendation.at[count, 'url'] = df_recipes['recipe_urls'][i]
        recommendation.at[count, 'score'] = "{:.3f}".format(float(scores[i]))
        count += 1
        if count==N:
            break
    return recommendation

def rec_sys(ingredients, difficulty, diet, N=5):
    with open('model/tfidf_encoding.pkl', 'rb') as f:
        tfidf_encodings = pickle.load(f)
    with open("model/tfidf_model.pkl", "rb") as f:
        tfidf = pickle.load(f)
    try: 
        ingredients_parsed = ingredient_parser(ingredients)
    except:
        ingredients_parsed = ingredient_parser([ingredients])
    ingredients_tfidf = tfidf.transform([ingredients_parsed])
    cos_sim = map(lambda x: cosine_similarity(ingredients_tfidf, x), tfidf_encodings)
    scores = list(cos_sim)
    recommendations = get_recommendations(N, scores, diet, difficulty)
    return recommendations

# if __name__ == "__main__":
#     ingredients = "rice, onion, garlic, peas"
#     difficulty = "Showing off"
#     diet = ['glutenfree','vegetarian']
#     recs = rec_sys(ingredients, difficulty, diet)
#     print(recs)
