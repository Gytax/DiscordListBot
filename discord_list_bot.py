import discord
from discord import app_commands
from discord_list import DiscordList
import json

class DiscordListBot(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.json_file_path = 'lists.json'
        self.tree = app_commands.CommandTree(self)
        self.lists = []
        self.read_from_file()

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

    async def delete_list(self, list: DiscordList):
        channel: discord.TextChannel = self.get_channel(list.channel_id)
        self.lists.remove(list)
        await channel.delete()
        self.save_to_file()

    def add_item_to_list(self, list: DiscordList, item: str):
        list.add_item(item)
        self.save_to_file()

    def remove_item_from_list(self, list: DiscordList, item: str):
        list.remove_item(item)
        self.save_to_file()

    def get_list(self, channel_id):
        return next(filter(lambda list: list.channel_id == channel_id, self.lists), None)

    def get_list_by_name(self, list_name):
        return next(filter(lambda list: list.name == list_name, self.lists), None)

    def read_from_file(self):
        with open(self.json_file_path) as openfile:
            json_lists = json.load(openfile)

        for json_list in json_lists:
            dl = DiscordList(json_list['name'], json_list['channel_id'])
            for item in json_list['items']:
                dl.add_item(item)
            self.lists.append(dl)

    def save_to_file(self):
        formatted = []
        for list in self.lists:
            formatted.append(list.format())

        json_object = json.dumps(formatted, indent=4)
        with open(self.json_file_path, 'w') as outfile:
            outfile.write(json_object)
