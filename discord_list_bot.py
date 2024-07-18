import discord
from discord import app_commands
from discord_list import DiscordList
import json

import logging

class DiscordListBot(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.json_file_path = 'lists.json'
        self.tree = app_commands.CommandTree(self)
        self.lists = []
        # self.read_from_file()

    async def on_ready(self):
        print(f'DiscordListBot logged in as {self.user}!')

    async def on_message(self, message):
        print(f'DiscordListBot received message from {message.author}: {message.content}')

    async def setup_hook(self):
        await self.tree.sync()

    async def new_list(self, interaction: discord.Interaction, name: str):
        # create a new channel with the name
        channel: discord.TextChannel = await interaction.guild.create_text_channel(name)
        self.lists.append(DiscordList(channel.name, channel.id))
        self.save_to_file()

    async def delete_list(self, interaction: discord.Interaction):
        channel: discord.TextChannel = self.get_channel(interaction.channel_id)
        self.lists.remove(DiscordList(channel.name, channel.id))
        await channel.delete()
        self.save_to_file()

    def get_list(self, channel_id):
        for list in self.lists:
            if list.channel_id == channel_id:
                return list
            else:
                return None

    def read_from_file(self):
        with open(self.json_file_path, 'r') as openfile:
            json.load(openfile)

    def save_to_file(self):
        formatted = []
        for list in self.lists:
            formatted.append(list)
        json_object = json.dumps(formatted, indent=4)
        with open(self.json_file_path, 'w') as outfile:
            outfile.write(json_object)
