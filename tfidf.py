import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle 

df_recipes = pd.read_csv('input_data/parsed_ingreds_recipes.csv')
df_recipes['ingredients_parsed'] = df_recipes.ingredients_parsed.values.astype('U')

tfidf = TfidfVectorizer()
tfidf.fit(df_recipes['ingredients_parsed'])
tfidf_recipe = tfidf.transform(df_recipes['ingredients_parsed'])

with open("model/tfidf_model.pkl", "wb") as f:
    pickle.dump(tfidf, f)

with open("model/tfidf_encoding.pkl", "wb") as f:
    pickle.dump(tfidf_recipe, f)
