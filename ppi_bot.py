import openai_secret_manager
import discord
import schedule
import time
import requests
import json

# Get secrets
secrets = openai_secret_manager.get_secrets("discord_bot")

# Initialize Discord client
client = discord.Client()

# Event listener for when the bot is ready
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    schedule.every(15).minutes.do(announce_call)
    schedule.every().day.at("9:30").do(announce_call) #announce call at 9:30 am every day
    schedule.every().day.at("16:00").do(announce_call) #announce call at 4:00 pm every day

# Event listener for when a message is sent
@client.event
async def on_message(message):
    # Check if message is from the bot
    if message.author == client.user:
        return

def announce_call():
    """Announce the best stock to buy based on current market readings to the server"""
    stock_to_buy = get_best_stock_to_buy()
    # Send the stock to the server
    for guild in client.guilds:
        for channel in guild.channels:
            if channel.name == 'general':
                await channel.send(f"Best stock to buy: {stock_to_buy}")

def get_best_stock_to_buy():
    """Get the best stock to buy based on current market readings"""
    # Get current market readings
    market_data = get_market_data()
    # Use best stock market strategy to determine the best stock to buy
    best_stock = ""
    best_stock_value = 0
    for stock in market_data:
        if stock["value"] > best_stock_value:
            best_stock = stock["name"]
            best_stock_value = stock["value"]
    return best_stock

def get_market_data():
    """Get current market data"""
    # Make a request to the market data API
    response = requests.get("https://marketdataapi.com/data")
    # Parse the JSON response
    market_data = json.loads(response.text)
    return market_data

# Run the bot
client.run(secrets["token"])

while True:
    schedule.run_pending()
    time.sleep(1)
