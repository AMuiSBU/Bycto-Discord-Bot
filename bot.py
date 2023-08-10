import discord
from discord.ext import commands
from discord import app_commands
import requests
from config import token, ebay_token

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
async def ebay(interaction: discord.Interaction, query: str, limit: int):
    # Replace spaces in query with '+' for url
    editedQuery = query.replace(" ", "+")
    # Construct url string with query and limit input
    url = f"https://api.ebay.com/buy/browse/v1/item_summary/search?q={editedQuery}&limit={limit}"
    # Construct headers with ebay application token and set desired eBay marketplace location
    headers = {
        "Authorization": f"Bearer {ebay_token}",
        "X-EBAY-C-MARKETPLACE-ID": "EBAY_US",
    }
    # Send request and store response
    response = requests.get(url, headers=headers)
    # Check for successful response
    if response.status_code == 200:
        data = response.json()

        # store the total number of query results
        total_results = data['total']

        # if total results is less than the limit, display the total number of results
        if total_results < limit:
            limit = total_results

        # initialize message to be sent
        reply_message = f'Searched for: {query}\nTotal Results: {total_results}\nDisplaying first {limit} results:'

        item_index = 1

        # display the name and price of each item
        for items in data['itemSummaries']:
            name = items['title']
            price = items['price']['value'] + ' ' + items['price']['currency']
            product_info = str(item_index) + '. ' + name + '\nPrice: ' + price
            itemLink = items['itemWebUrl']
            linkString = f'[Click to View]({itemLink})'
            reply_message = reply_message + f'\n{product_info}' + f' | {linkString}'
            item_index = item_index + 1

        await interaction.response.send_message(reply_message, suppress_embeds=True)

    else:
        print("Error:", response.status_code)
        print(response.text)
        await interaction.response.send_message('Failure to obtain response')

bot.run(token)
