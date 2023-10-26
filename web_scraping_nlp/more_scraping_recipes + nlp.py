import requests
from bs4 import BeautifulSoup
import pandas as pd 
import numpy as np
import nltk
import string
import ast
import re
import unidecode
nltk.download('stopwords')
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

headers = {'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.58"}

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
            count=0
            for label in self.soup.find_all('div', {'class': 'mntl-recipe-details__label'}):
                if label.text.strip() == 'Servings:':
                    return self.soup.find_all('div', {'class': 'mntl-recipe-details__value'})[count].text.strip()
                count+=1
        except:
            return np.nan 

    def cooking_time(self):
        try:
            count=0
            for label in self.soup.find_all('div', {'class': 'mntl-recipe-details__label'}):
                if label.text.strip() == 'Total Time:':
                    return self.soup.find_all('div', {'class': 'mntl-recipe-details__value'})[count].text.strip()
                count+=1
        except:
            return np.nan

    def difficulty(self):
        try:
            count=0
            for label in self.soup.find_all('div', {'class': 'mntl-recipe-details__label'}):
                if label.text.strip() == 'Prep Time:':
                    minute = int(self.soup.find_all('div', {'class': 'mntl-recipe-details__value'})[count].text.strip().split(' ')[0])
                    break
                count+=1
            if minute<=15:
                level='Super easy'
            elif minute<=30:
                level='Not too tricky'
            else:
                level='Showing off'
            return level
        except:
            return np.nan
    
    def diet(self):
        try:
            gluten = ['wheat','barley','rye','spelt','kamut','triticale','durum','semolina','farro','bulgur','malt','couscous','wheat germ','wheat bran','wheat starch','matzo','pasta','flour','breadcrumb','cracker','pretzel','cookie','cake','muffin','biscuit','croissant','doughnut','pancake',
                                      'waffle',
                                        'bread',
                                        'dough',
                                        'tortilla',
                                        'wrap',
                                        'beer',
                                        'ale',
                                        'lager',
                                        'stout',
                                        'malt vinegar',
                                        'malt extract',
                                        'malt flavoring',
                                        'matzo meal',
                                        'communion wafers']
            dairy = ['milk',
                                              'butter',
                                              'cream',
                                                'cheese',
                                                'yogurt',
                                                'buttermilk',
                                                'sour cream',
                                                'cottage cheese',
                                                'whey',
                                                'curds',
                                                'malted milk',
                                                'margarine',
                                                'ghee',
                                                'powdered milk',
                                                'evaporated milk',
                                                'condensed milk',
                                                'ice cream',
                                                'sherbet',
                                                'gelato',
                                                'pudding',
                                                'custard',
                                                'cream cheese',
                                                'processed cheese',
                                                'whey protein',
                                                'chocolate']
            vegetarian = ['meat',
                          'beef',
                            'pork',
                            'lamb',
                            'veal',
                            'mutton',
                            'goat',
                            'poultry',
                            'chicken',
                            'turkey',
                            'duck',
                            'quail',
                            'guinea fowl',
                            'game birds',
                            'fish',
                            'shellfish',
                            'crab',
                            'lobster',
                            'shrimp',
                            'prawn',
                            'clams',
                            'mussels',
                            'oysters',
                            'scallops',
                            'squid',
                            'octopus',
                            'anchovies',
                            'anchovy'
                            'herring',
                            'sardines',
                            'tuna',
                            'salmon',
                            'trout',
                            'cod',
                            'tilapia',
                            'catfish',
                            'swordfish',
                            'mahi-mahi',
                            'snapper',
                            'bass',
                            'sole',
                            'flounder',
                            'sole',
                            'haddock',
                            'pollock',
                            'whitefish',
                            'caviar',
                            'fish sauce',
                            'oyster sauce',
                            'anchovy paste',
                            'egg',
                            'gelatin',
                            'lard',
                            'rennet',
                            'tallow',
                            'suet']
            vegan = ['milk',
                     'butter',
                                              'cream',
                                                'cheese',
                                                'yogurt',
                                                'buttermilk',
                                                'sour cream',
                                                'cottage cheese',
                                                'whey',
                                                'curds',
                                                'malted milk',
                                                'margarine',
                                                'ghee',
                                                'powdered milk',
                                                'evaporated milk',
                                                'condensed milk',
                                                'ice cream',
                                                'sherbet',
                                                'gelato',
                                                'pudding',
                                                'custard',
                                                'cream cheese',
                                                'processed cheese',
                                                'whey protein',
                                                'chocolate',
                                                'meat',
                          'beef',
                            'pork',
                            'lamb',
                            'veal',
                            'mutton',
                            'goat',
                            'poultry',
                            'chicken',
                            'turkey',
                            'duck',
                            'quail',
                            'guinea fowl',
                            'game birds',
                            'fish',
                            'shellfish',
                            'crab',
                            'lobster',
                            'shrimp',
                            'prawn',
                            'clams',
                            'mussels',
                            'oysters',
                            'scallops',
                            'squid',
                            'octopus',
                            'anchovies',
                            'anchovy'
                            'herring',
                            'sardines',
                            'tuna',
                            'salmon',
                            'trout',
                            'cod',
                            'tilapia',
                            'catfish',
                            'swordfish',
                            'mahi-mahi',
                            'snapper',
                            'bass',
                            'sole',
                            'flounder',
                            'sole',
                            'haddock',
                            'pollock',
                            'whitefish',
                            'caviar',
                            'fish sauce',
                            'oyster sauce',
                            'anchovy paste',
                            'egg',
                            'gelatin',
                            'lard',
                            'rennet',
                            'tallow',
                            'suet',
                     'honey',
                     'beeswax']

            parsed_ingreds = self.ingredient_parser()
            diet_list = []
            if 'dairy' in parsed_ingreds:
                diet_list.append('dairyfree')
            else:
                count = 0
                for i in dairy:
                    if i in parsed_ingreds:
                        count+=1
                        break
                if count==0:
                    diet_list.append('dairyfree')
            if 'gluten' in parsed_ingreds:
                diet_list.append('glutenfree')
            else:
                count = 0
                for i in gluten:
                    if i in parsed_ingreds:
                        count+=1
                        break
                if count==0:
                    diet_list.append('glutenfree')
            if 'vegetarian' in parsed_ingreds:
                diet_list.append('vegetarian')
            else:
                count = 0
                for i in vegetarian:
                    if i in parsed_ingreds:
                        count+=1
                        break
                if count==0:
                    diet_list.append('vegetarian')
            if 'vegan' in parsed_ingreds:
                diet_list.append('vegan')
            else:
                count = 0
                for i in vegan:
                    if i in parsed_ingreds:
                        count+=1
                        break
                if count==0:
                    diet_list.append('vegan')
            return diet_list
        except:
            return np.nan

    def ingredients(self):
        try:
            ing_list = self.soup.find_all('ul', {'class': 'mntl-structured-ingredients__list'})
            ingred_list = []
            for i in ing_list:
                ingred_list += [ing for ing in i.text.split('\n') if ing!='']
            return ingred_list
        except:
            return np.nan
    
    def ingredient_parser(self):
        ingreds = self.ingredients()
        measures = ['teaspoon', 't', 'tsp.', 'tablespoon', 'T', 'tbl.', 'tb', 'tbsp.', 'fluid ounce', 'fl oz', 'gill', 'cup', 'c', 'pint', 'p', 'pt', 'fl pt', 'quart', 'q', 'qt', 'fl qt', 'gallon', 'g', 'gal', 'ml', 'milliliter', 'millilitre', 'cc', 'mL', 'l', 'liter', 'litre', 'L', 'dl', 'deciliter', 'decilitre', 'dL', 'bulb', 'level', 'heaped', 'rounded', 'whole', 'pinch', 'medium', 'slice', 'pound', 'lb', '#', 'ounce', 'oz', 'mg', 'milligram', 'milligramme', 'g', 'gram', 'gramme', 'kg', 'kilogram', 'kilogramme', 'x', 'of', 'mm', 'millimetre', 'millimeter', 'cm', 'centimeter', 'centimetre', 'm', 'meter', 'metre', 'inch', 'in', 'milli', 'centi', 'deci', 'hecto', 'kilo']
        # words_to_remove = ['fresh', 'oil', 'a', 'red', 'bunch', 'and', 'clove', 'or', 'leaf', 'chilli', 'large', 'extra', 'sprig', 'ground', 'handful', 'free', 'small', 'pepper', 'virgin', 'range', 'from', 'dried', 'sustainable', 'black', 'peeled', 'higher', 'welfare', 'seed', 'for', 'finely', 'freshly', 'sea', 'quality', 'white', 'ripe', 'few', 'piece', 'source', 'to', 'organic', 'flat', 'smoked', 'ginger', 'sliced', 'green', 'picked', 'the', 'stick', 'plain', 'plus', 'mixed', 'mint', 'bay', 'basil', 'your', 'cumin', 'optional', 'fennel', 'serve', 'mustard', 'unsalted', 'baby', 'paprika', 'fat', 'ask', 'natural', 'skin', 'roughly', 'into', 'such', 'cut', 'good', 'brown', 'grated', 'trimmed', 'oregano', 'powder', 'yellow', 'dusting', 'knob', 'frozen', 'on', 'deseeded', 'low', 'runny', 'balsamic', 'cooked', 'streaky', 'nutmeg', 'sage', 'rasher', 'zest', 'pin', 'groundnut', 'breadcrumb', 'turmeric', 'halved', 'grating', 'stalk', 'light', 'tinned', 'dry', 'soft', 'rocket', 'bone', 'colour', 'washed', 'skinless', 'leftover', 'splash', 'removed', 'dijon', 'thick', 'big', 'hot', 'drained', 'sized', 'chestnut', 'watercress', 'fishmonger', 'english', 'dill', 'caper', 'raw', 'worcestershire', 'flake', 'cider', 'cayenne', 'tbsp', 'leg', 'pine', 'wild', 'if', 'fine', 'herb', 'almond', 'shoulder', 'cube', 'dressing', 'with', 'chunk', 'spice', 'thumb', 'garam', 'new', 'little', 'punnet', 'peppercorn', 'shelled', 'saffron', 'other''chopped', 'salt', 'olive', 'taste', 'can', 'sauce', 'water', 'diced', 'package', 'italian', 'shredded', 'divided', 'parsley', 'vinegar', 'all', 'purpose', 'crushed', 'juice', 'more', 'coriander', 'bell', 'needed', 'thinly', 'boneless', 'half', 'thyme', 'cubed', 'cinnamon', 'cilantro', 'jar', 'seasoning', 'rosemary', 'extract', 'sweet', 'baking', 'beaten', 'heavy', 'seeded', 'tin', 'vanilla', 'uncooked', 'crumb', 'style', 'thin', 'nut', 'coarsely', 'spring', 'chili', 'cornstarch', 'strip', 'cardamom', 'rinsed', 'honey', 'cherry', 'root', 'quartered', 'head', 'softened', 'container', 'crumbled', 'frying', 'lean', 'cooking', 'roasted', 'warm', 'whipping', 'thawed', 'corn', 'pitted', 'sun', 'kosher', 'bite', 'toasted', 'lasagna', 'split', 'melted', 'degree', 'lengthwise', 'romano', 'packed', 'pod', 'anchovy', 'rom', 'prepared', 'juiced', 'fluid', 'floret', 'room', 'active', 'seasoned', 'mix', 'deveined', 'lightly', 'anise', 'thai', 'size', 'unsweetened', 'torn', 'wedge', 'sour', 'basmati', 'marinara', 'dark', 'temperature', 'garnish', 'bouillon', 'loaf', 'shell', 'reggiano', 'canola', 'parmigiano', 'round', 'canned', 'ghee', 'crust', 'long', 'broken', 'ketchup', 'bulk', 'cleaned', 'condensed', 'sherry', 'provolone', 'cold', 'soda', 'cottage', 'spray', 'tamarind', 'pecorino', 'shortening', 'part', 'bottle', 'sodium', 'cocoa', 'grain', 'french', 'roast', 'stem', 'link', 'firm', 'asafoetida', 'mild', 'dash', 'boiling']
        words_to_remove = ['fillet', 'skinless', 'boned', 'iceburg', 'iceberg', 'olive', 'fresh', 'oil', 'a', 'red', 'bunch', 'and', 'clove', 'or', 'groundnut', 'leaf', 'chilli', 'large', 'extra', 'sprig', 'ground', 'handful', 'free', 'small', 'pepper', 'virgin', 'range', 'from', 'dried', 'sustainable', 'black', 'peeled', 'higher', 'welfare', 'seed', 'for', 'finely', 'freshly', 'sea', 'quality', 'white', 'ripe', 'few', 'piece', 'source', 'to', 'organic', 'flat', 'smoked', 'sliced', 'green', 'picked', 'the', 'stick', 'plain', 'plus', 'mixed', 'your', 'optional', 'serve', 'mustard', 'unsalted', 'baby', 'paprika', 'fat', 'ask', 'natural', 'skin', 'roughly', 'into', 'such', 'cut', 'good', 'brown', 'grated', 'trimmed', 'powder', 'yellow', 'dusting', 'knob', 'frozen', 'on', 'deseeded', 'low', 'runny', 'balsamic', 'cooked', 'streaky', 'rasher', 'zest', 'pin', 'breadcrumb', 'halved', 'grating', 'stalk', 'light', 'tinned', 'dry', 'soft', 'rocket', 'bone', 'colour', 'washed', 'skinless', 'leftover', 'splash', 'removed', 'dijon', 'thick', 'big', 'hot', 'drained', 'sized', 'chestnut', 'watercress', 'fishmonger', 'english', 'raw', 'flake', 'cider', 'cayenne', 'tbsp', 'leg', 'pine', 'wild', 'if', 'fine', 'herb', 'shoulder', 'cube', 'dressing', 'with', 'chunk', 'spice', 'thumb', 'garam', 'new', 'little', 'punnet', 'peppercorn', 'shelled', 'saffron', 'other', 'chopped', 'salt', 'taste', 'can', 'sauce', 'water', 'diced', 'package', 'italian', 'shredded', 'divided', 'all', 'purpose', 'crushed', 'juice', 'more', 'bell', 'needed', 'thinly', 'boneless', 'half', 'cubed', 'jar', 'seasoning', 'extract', 'baking', 'beaten', 'heavy', 'seeded', 'tin', 'uncooked', 'crumb', 'style', 'thin', 'coarsely', 'spring', 'strip', 'rinsed', 'root', 'quartered', 'head', 'softened', 'container', 'crumbled', 'frying', 'lean', 'cooking', 'roasted', 'warm', 'whipping', 'thawed', 'pitted', 'sun', 'kosher', 'bite', 'toasted', 'split', 'melted', 'degree', 'lengthwise', 'romano', 'packed', 'pod', 'rom', 'prepared', 'juiced', 'fluid', 'floret', 'room', 'active', 'seasoned', 'mix', 'deveined', 'lightly', 'thai', 'size', 'unsweetened', 'torn', 'wedge', 'sour', 'basmati', 'dark', 'temperature', 'garnish', 'loaf', 'shell', 'reggiano', 'canola', 'parmigiano', 'round', 'canned', 'ghee', 'crust', 'long', 'broken', 'bulk', 'cleaned', 'provolone', 'cold', 'spray', 'part', 'bottle', 'sodium', 'grain', 'french', 'roast', 'stem', 'link', 'firm', 'mild', 'dash', 'boiling']

        if isinstance(ingreds, list):
            ingredients = ingreds
        else:
            ingredients = ast.literal_eval(ingreds)

        translator = str.maketrans('', '', string.punctuation)
        lemmatizer = WordNetLemmatizer()

        ingred_list = []
        for i in ingredients:
            i.translate(translator)
            items = re.split(' |-', i)
            items = [word for word in items if word.isalpha()]
            items = [word.lower() for word in items]
            items = [unidecode.unidecode(word) for word in items]
            items = [lemmatizer.lemmatize(word) for word in items]
            stop_words = set(stopwords.words('english'))
            items = [word for word in items if word not in stop_words]
            items = [word for word in items if word not in measures]
            items = [word for word in items if word not in words_to_remove]
            if items:
                ingred_list.append(' '.join(items)) 

        ingred_list = " ".join(ingred_list)
        return ingred_list


recipe_df = pd.read_csv("more_recipes_urls.csv")

attributes = ['recipe_name', 'serves', 'cooking_time', 'difficulty', 'diet', 'ingredients', 'ingredient_parser']

temp_df = pd.DataFrame(columns=['recipe_name', 'serves', 'cooking_time', 'difficulty', 'diet', 'ingredients', 'ingredients_parsed'])

for i in range(len(recipe_df['recipe_urls'])):
    url = recipe_df['recipe_urls'][i]
    recipe_scraper = RecipeScraping(url)
    temp_df.loc[i] = [getattr(recipe_scraper, attribute)() for attribute in attributes]
    if i % 100 == 0:
        print(f'Step {i} completed')

temp_df['recipe_urls'] = recipe_df['recipe_urls']
columns = ['recipe_urls'] + ['recipe_name', 'serves', 'cooking_time', 'difficulty', 'diet', 'ingredients', 'ingredients_parsed']
final_recipe_df = temp_df[columns]
final_recipe_df.to_csv("input_data/more_recipes_data.csv", index=False)
