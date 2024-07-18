import discord
from discord import app_commands
import os

from discord_list_bot import DiscordListBot

client: DiscordListBot = DiscordListBot(intents=discord.Intents.default())

@app_commands.command(name='new-list', description='Creates a new channel, holding the list')
@app_commands.describe(name='Name of the list')
async def new_list(interaction: discord.Interaction, name: str):
    await client.new_list(interaction, name)
    await interaction.response.send_message(f'I have created the list {name} for you!', ephemeral=True)

@app_commands.command(name='delete-list', description='Delete the current list channel')
async def delete_list(interaction: discord.Interaction):
    list = client.get_list(interaction.channel_id)
    if list:
        await client.delete_list(list)
        message = 'List deleted!'
    else:
        message = 'This channel is not a list channel!'
    await interaction.response.send_message(message, ephemeral=True)

@app_commands.command(name='add-item', description='Add an item to a list')
@app_commands.describe(list='Name of the list', item='Name of the item to add')
async def add_item(interaction: discord.Interaction, list: str, item: str):
    discord_list = client.get_list_by_name(list)
    if discord_list:
        message = 'Item {item} added to list {list}'.format(item=item, list=list)
        client.add_item_to_list(discord_list, item)
    else:
        message = 'Channel not found!'
    await interaction.response.send_message(message, ephemeral=True)

@app_commands.command(name='remove-item', description='Remove an item from a list')
@app_commands.describe(list='Name of the list', item='Name of the item to remove')
async def add_item(interaction: discord.Interaction, list: str, item: str):
    discord_list = client.get_list_by_name(list)
    if discord_list:
        message = 'Item {item} removed from list {list}'.format(item=item, list=list)
        client.remove_item_from_list(discord_list, item)
    else:
        message = 'Channel not found!'
    await interaction.response.send_message(message, ephemeral=True)

client.run(os.environ.get('BOT_TOKEN'))
