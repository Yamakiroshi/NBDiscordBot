import os
import discord
from dotenv import load_dotenv
import psycopg2
import requests
import json
load_dotenv()


def get_random_cat_image(categories):
    url = "https://api.thecatapi.com/v1/images/search"
    if categories != "":
        url += categories
    headers = {
        "x-api-key":os.getenv('CAT_KEY')
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = json.loads(response.text)
        if data and len(data) > 0:
            cat_image_url = data[0]['url']
            return cat_image_url
        else:
            return "No cat images found."
    else:
        return "Failed to retrieve a cat image."

def get_cat_categories():
    url = "https://api.thecatapi.com/v1/categories"
    headers = {
        "x-api-key":os.getenv('CAT_KEY')
    }

    response = requests.get(url,headers = headers)
    if response.status_code == 200:
        data = json.loads(response.text)
        if data and len(data) > 0:
            return data

def get_category_id(searchTerm):
    for item in cat_categories:
        if item['name'] == searchTerm:
            result_id = item['id']
            break

    if result_id is not None:
        return result_id
    else:
        return ""
    
def compile_category_string(search_terms):
    categories = []
    for term in search_terms:
        category = get_category_id(term)
        if category != "":
            categories.append(category)

    if len(categories) > 1:
        categories = ','.join(map(str,categories))
    else:
        categories = categories[0]
    
    return f"?category_ids={categories}"


class NoodleBowlBotClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')
        if message.author.id == self.user.id:
            return

        if message.content.startswith('$cat'):
            categories = ""
            splitstring = message.content.split(" ")
            splitstring.pop(0)
            if len(splitstring) > 0:
                categories = compile_category_string(splitstring)

            cat_url = get_random_cat_image(categories=categories)
            await message.channel.send(f"Random Cat Picture:\n{cat_url}")

        if message.content.startswith('$morecats'):
            get_cat_categories()


intents = discord.Intents.default()
intents.message_content = True

conn = psycopg2.connect(host=os.getenv('DB_HOST'), database=os.getenv('DB_DB'), user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'), port=os.getenv('DB_PORT'))
cat_categories = get_cat_categories()


client = NoodleBowlBotClient(intents=intents)
client.run(os.getenv('DISCORD_TOKEN'))