import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

recipe_url_df = pd.Series()

for i in range(10):
    urls = ['https://www.allrecipes.com/recipes/78/breakfast-and-brunch/',
           'https://www.allrecipes.com/recipes/17561/lunch/',
           'https://www.allrecipes.com/recipes/84/healthy-recipes/',
           'https://www.allrecipes.com/recipes/76/appetizers-and-snacks/',
           'https://www.allrecipes.com/recipes/96/salad/',
           'https://www.allrecipes.com/recipes/81/side-dish/',
           'https://www.allrecipes.com/recipes/16369/soups-stews-and-chili/soup/',
           'https://www.allrecipes.com/recipes/156/bread/',
           'https://www.allrecipes.com/recipes/77/drinks/',
           'https://www.allrecipes.com/recipes/79/desserts/']
    url = urls[i]
    headers = {'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.58"}
    pattern = r'\d+(.*)'
    match = re.search(pattern, url)
    url_pattern = match.group(1)
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    recipe_urls = pd.Series([a.get("href")for a in soup.find_all("a")])
    recipe_urls = pd.Series(recipe_urls[(recipe_urls.str.startswith("https://www.allrecipes.com/recipes/")==True) & (recipe_urls.str.contains(r'\d')==True) & (recipe_urls.str.contains(url_pattern)==True)].unique()[1:])
    recipe_url_df = pd.concat([recipe_url_df, recipe_urls], ignore_index=True)

recipes_urls = pd.Series()
for i in recipe_url_df:
    url = i
    headers = {'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.58"}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    recipe_urls = pd.Series([a.get("href")for a in soup.find_all("a")])
    recipe_urls = pd.Series(recipe_urls[(recipe_urls.str.startswith("https://www.allrecipes.com/recipes/")==True) & (recipe_urls.str.contains(r'\d')==True)].unique())
    recipes_urls = pd.concat([recipes_urls, recipe_urls], ignore_index=True)

recipes_urls_df = pd.DataFrame(recipes_urls, columns=['recipe_urls'])
recipes_urls_df.to_csv('more_recipe_urls.csv', index=False)
