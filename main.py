import discord
from discord import app_commands
import os

from discord_list_bot import DiscordListBot

client: DiscordListBot = DiscordListBot(intents=discord.Intents.default())

# @client.tree.command()
# async def hello(interaction: discord.Interaction):
#     """Says hello!"""
#     await interaction.response.send_message(f'Hi, {interaction.user.mention}')

# @client.tree.command()
# @app_commands.describe(first='The first number to add', second='The second number to add')
# async def add(
#     interaction: discord.Interaction,
#     # This makes it so the first parameter can only be between 0 to 100.
#     first: app_commands.Range[int, 0, 100],
#     # This makes it so the second parameter must be over 0, with no maximum limit.
#     second: app_commands.Range[int, 0, None],
# ):
#     """Adds two numbers together"""
#     await interaction.response.send_message(f'{first} + {second} = {first + second}', ephemeral=True)

@client.tree.command(name="new-list", description="Creates a new channel, holding the list")
@app_commands.describe(name='Name of the list')
async def new_list(interaction: discord.Interaction, name: str):
    await client.new_list(interaction, name)
    await interaction.response.send_message(f'I have created the list {name} for you!', ephemeral=True)

@client.tree.command(name="delete-list", description="Delete the current list channel")
async def delete_list(interaction: discord.Interaction):
    if client.get_list(interaction.channel_id):
        await client.delete_list(interaction)
        message = 'List deleted!'
    else:
        message = 'This channel is not a list channel!'
    await interaction.response.send_message(message, ephemeral=True)

client.run(os.environ.get('BOT_TOKEN', token))
