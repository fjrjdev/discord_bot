import json
import os
import random

import discord
import dotenv
import requests


dotenv.load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]["q"] + " -" + json_data[0]["a"]
    return quote


def get_find(param):
    response = requests.get(f"https://simple-spotify-api.herokuapp.com/?search={param}")
    json_data = json.loads(response.text)
    print(json_data["data"][0]["music_url"])
    return json_data["data"][0]["music_url"]


meme_words = ["Drake", "Is this a...?", "This is fine"]
res_words = ["Ta loco", "Hotlime bling"]


@client.event
async def on_ready():
    print("we have llogged in as{0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    msg = message.content
    if msg.startswith("$hello"):
        await message.channel.send("Hello Word!")

    if msg.startswith("$inspire"):
        quote = get_quote()
        await message.channel.send(quote)
    if msg.startswith("$find"):
        search = msg[6::]
        response = get_find(search)
        await message.channel.send(response)

    if any(word in msg for word in meme_words):
        await message.channel.send(random.choice(res_words))


client.run(os.getenv("TOKEN"))
