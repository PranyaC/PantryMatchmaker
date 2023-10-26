import requests
from bs4 import BeautifulSoup
import pandas as pd 
import numpy as np

headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.51"}

class RecipeScraping():

    def __init__(self, url):
        self.url = url 
        self.soup = BeautifulSoup(requests.get(url, headers=headers).content, 'html.parser')
    
    def recipe_name(self):
        try:
            return self.soup.find('h1').text.strip()
        except: 
            return np.nan
        
    def serves(self):
        try:
            return self.soup.find('div', {'class': 'recipe-detail serves'}).text.split()[2]
        except:
            return np.nan 

    def cooking_time(self):
        try:
            return self.soup.find('div', {'class': 'recipe-detail time'}).text.split('In')[1].strip()
        except:
            return np.nan

    def difficulty(self):
        try:
            return self.soup.find('div', {'class': 'col-md-12 recipe-details-col remove-left-col-padding-md'}).text.split('Difficulty')[1].strip()
        except:
            return np.nan
    
    def diet(self):
        try:
            diet_list = self.soup.find('div', {'class':'special-diets-wrapper'}).text.split()
            for d in range(len(diet_list)):
                if diet_list[d] == 'Gluten-freegf':
                    diet_list[d] = 'glutenfree'
                elif diet_list[d] == 'Dairy-freedf':
                    diet_list[d] = 'dairyfree'
                elif diet_list[d] == 'Vegetarianv':
                    diet_list[d] = 'vegetarian'
                elif diet_list[d] == 'Veganvg':
                    diet_list[d] = 'vegan'
            return diet_list
        except:
            return np.nan

    def ingredients(self):
        try:
            ingredients = [] 
            for li in self.soup.select('.ingred-list li'):
                ingred = ' '.join(li.text.split())
                ingredients.append(ingred)
            return ingredients
        except:
            return np.nan


recipe_df = pd.read_csv("input_data/recipe_urls.csv")

attributes = ['recipe_name', 'serves', 'cooking_time', 'difficulty', 'diet', 'ingredients']

temp_df = pd.DataFrame(columns=attributes)

for i in range(len(recipe_df['recipe_urls'])):
    url = recipe_df['recipe_urls'][i]
    recipe_scraper = RecipeScraping(url)
    temp_df.loc[i] = [getattr(recipe_scraper, attribute)() for attribute in attributes]
    if i % 100 == 0:
        print(f'Step {i} completed')

temp_df['recipe_urls'] = recipe_df['recipe_urls']
columns = ['recipe_urls'] + attributes
final_recipe_df = temp_df[columns]

final_recipe_df.to_csv("input_data/recipes_data.csv", index=False)
