import discord
from discord.ext import commands
from discord import app_commands
from config import token
from ebay_browser import ebay_api_call
from requests_cache import CachedSession

bot = commands.Bot(command_prefix='.', intents=discord.Intents.all())


@bot.event
async def on_ready():
    print(f'{bot.user} is running')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)


@bot.tree.command(name="ebay", description='Search for items on eBay')
@app_commands.describe(query='Search query', limit='Number of results')
async def ebayBrowse(interaction: discord.Interaction, query: str, limit: int):
    # Create session with caching capabilities
    session_cache = CachedSession('api_cache', expire_after=300)
    # Send request and store response
    response = ebay_api_call(session_cache, query, limit)
    # Check for successful response
    if response.status_code == 200:
        data = response.json()

        # Store the total number of query results
        total_results = data['total']

        # If total results is less than the limit, display the total number of results
        if total_results < limit:
            limit = total_results

        # Initialize message to be sent
        embed = discord.Embed(title=f'Searched for: {query}',
                              description=f'Total Results: {total_results}\nDisplaying first {limit} results:',
                              colour=0x000000)

        item_index = 1

        # Display the name and price of each item
        for items in data['itemSummaries']:
            name = str(item_index) + '. ' + items['title']
            price = items['price']['value'] + ' ' + items['price']['currency']
            itemLink = items['itemWebUrl']
            linkString = f'[Click to View]({itemLink})'
            embed.add_field(name=name, value=f'\nPrice: ' + price + ' | ' + f'{linkString}', inline=False)
            item_index = item_index + 1

        await interaction.response.send_message(embed=embed)

    else:
        print("Error:", response.status_code)
        print(response.text)
        await interaction.response.send_message('Failure to obtain response')


bot.run(token)
