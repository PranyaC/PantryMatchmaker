ingredients = ['onion', 'tomato', 'garlic', 'peas', 'rice']


# response = get_completion(prompt)
# print(response)


# import openai
# openai.api_key = "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"

# completion = openai.ChatCompletion.create(
#   model="gpt-3.5-turbo",
#   messages=[
#     {"role": "system", "content": "You are a helpful assistant."},
#     {"role": "user", "content": "Hello!"}
#   ],
#   temperature=0.1
# )

# print(completion.choices[0].message)

from gpt4all import GPT4All
def generate_recipes(ingredients, difficulty, diet):
    model = GPT4All("orca-mini-3b-gguf2-q4_0.gguf")
    prompt = f"""
    Provided a list of ingredients, your task is to create a new recipe using all those ingredients 
    such that it satisfies the difficulty level and dietary requirements given as well. 
    Mention the name of the recipe, the ingredients required for the recipe and list all the steps required to make it.
    List of ingredients: ```{ingredients}```
    Difficulty level: ```{difficulty}```
    Dietary requirements: ```{diet}```
    """
    output = model.generate(prompt=prompt, temp=0.5)
    return output