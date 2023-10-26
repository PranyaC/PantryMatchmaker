import requests
from bs4 import BeautifulSoup
import pandas as pd

recipe_url_df = pd.DataFrame() 

food_cat = ["mains", "snacks", "breakfast", "desserts", "drinks", "sides"]

for cat in food_cat:

    url = f"https://www.jamieoliver.com/recipes/category/course/{cat}/"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")

    recipe_urls = pd.Series([a.get("href") for a in soup.find_all("a")])

    recipe_urls = recipe_urls[(recipe_urls.str.count("-")>0) 
                            & (recipe_urls.str.contains("/recipes/")==True)
                            & (recipe_urls.str.contains("-recipes/")==True)
                            & (recipe_urls.str.contains("course")==False)
                            & (recipe_urls.str.contains("books")==False)
                            & (recipe_urls.str.endswith("recipes/")==False)
                            ].unique()

    df = pd.DataFrame({"recipe_urls":recipe_urls})
    df['recipe_urls'] = "https://www.jamieoliver.com" + df['recipe_urls'].astype('str')
    recipe_url_df = recipe_url_df.append(df).copy()

recipe_url_df = recipe_url_df.drop_duplicates()
recipe_url_df.to_csv("input_data/recipe_urls.csv", sep="\t", index=False)
