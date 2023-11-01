'''
Core.py
Author: Adam Hay
Date Created: 18/10/2023

'''

from databasemanager import DatabaseManager, DatabaseUrlManager
import importlib
import os
from dotenv import load_dotenv
import discord
load_dotenv()

class NoodlebowlBot():
    def __init__(self,database_enable=False, **kwargs):
        print("helloWorld");
        '''
            This is what we're going to be using for the startup sequence
        '''
        self.cli_params = kwargs #This is to allow someone setting up the bot the allowance to create a plugin that can be controlled through cli arguments
        self.loaded_plugins = None # List of all the plugins that have been loaded into the system.

        # Bot Setup
        if database_enable: 
            database_url = DatabaseUrlManager(username=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'), database=os.getenv('DB_DB'), port=os.getenv('DB_PORT'), host=os.getenv('DB_HOST')).get_url()
            self.database_manager = DatabaseManager(database_url)
            self.database_conn = self.database_manager.connect()

        intents = discord.Intents.default()
        intents.message_content = True
        self.client = NoodlebowlBotClient(self.loaded_plugins,intents=intents)

        #Final Step Run the client
        self.run_discord_client()
    
    def run_discord_client(self):
        self.client.run(os.getenv('DISCORD_TOKEN'))

class NoodlebowlBotClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
    
    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')
        if message.author.id == self.user.id:
            return


if __name__ == "__main__":
    NoodlebowlBot(database_enable=True)
