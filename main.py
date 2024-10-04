import json
import random

import requests
import speedtest
from discord.ext import commands
from gnews import GNews
from jokeapi import Jokes
from pyrandmeme import *

import os
from dotenv import load_dotenv


DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
# -------------------------------------------------------------------------------------------------------
intents = discord.Intents.all()
intents.members = True

client = commands.Bot(command_prefix="!", intents=intents)
bot = commands.Bot(command_prefix="!", intents=intents)


@client.event
async def on_ready():
    print("!TAKASHI is awake!")
    print("-------------")


@client.command()
async def hello(ctx):
    await ctx.send("Hi, I am idle bbot!")


@client.event
async def on_member_join(members):
    channel = client.get_channel(1071039409434153054)
    await channel.send("Hello, here's your welcome joke!")
    j = await Jokes()
    jokes = await j.get_joke()
    if jokes["type"] == "single":
        await channel.send(jokes["joke"])
    else:
        await channel.send(jokes["setup"])
        await channel.send(jokes["delivery"])


@client.event
async def on_member_remove(members):
    channel = client.get_channel(1071039409434153054)
    await channel.send("Goodbye!\nSorry to see you go!")


@client.command()
async def ping(ctx):
    await ctx.send("pong")


@client.command()
async def meme(ctx):
    await ctx.send(embed=await pyrandmeme())


@client.command()
async def joke(ctx):
    j = await Jokes()
    jokes = await j.get_joke()
    if jokes["type"] == "single":
        await ctx.send(jokes["joke"])
    else:
        await ctx.send(jokes["setup"])
        await ctx.send(jokes["delivery"])


@client.command()
async def quote(ctx):
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    q = json_data[0]["q"] + " \n-" + json_data[0]["a"]
    await ctx.send(q)


@client.command(pass_context=True)
async def join(ctx):
    if ctx.author.voice:
        room = ctx.message.author.voice.channel
        await room.connect()
        await ctx.send("BOT joined.")
    else:
        await ctx.send("Sorry! You are not in a Voice Channel.")


@client.command(pass_context=True)
async def leave(ctx):
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
        await ctx.send("BOT left.")
    else:
        await ctx.send("Sorry! BOT is not present in a Voice Channel.")


@client.command()
async def flipacoin(ctx):
    await ctx.send(random.choice(["Heads", "Tails"]))


@client.command()
async def rolladice(ctx):
    await ctx.send(random.choice([1, 2, 3, 4, 5, 6]))


@client.command()
async def weather(ctx):
    API_Key = "0f385eb399cef4cbeb4d7020f3bce1d6"
    city_name = "Dhaka"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_Key}"
    response = requests.get(url)
    res = response.json()
    if res["cod"] != "404":
        data = res["main"]
        live_temperature = int(data["temp"]) - float(273.15)
        live_pressure = data["pressure"]
        desc = res["weather"]
        weather_description = desc[0]["description"]
        ltemp = f"Temperature: {live_temperature:.2f}{chr(176)}"
        lpress = f"Pressure: {str(live_pressure)}mb"
        des = f"Description: {str(weather_description)}"
        await ctx.send(ltemp)
        await ctx.send(lpress)
        await ctx.send(des)


@client.command()
async def speed(ctx):
    st = speedtest.Speedtest(secure=True)
    best = st.get_best_server()
    await ctx.send("Processing....")
    await ctx.send(f"Download speed: {(st.download() / (1024 * 1024)):.2f}Mbps")
    await ctx.send(f"Upload speed: {(st.upload() / (1024 * 1024)):.2f}Mbps")
    await ctx.send(f"Latency: {best['latency']:.2f}ms")


@client.command()
async def math_fact(ctx):
    maturl = "https://numbersapi.p.rapidapi.com/random/trivia"

    querystring = {"min": "0", "max": "1000", "fragment": "true", "json": "true"}

    headers = {
        "X-RapidAPI-Key": "38a88804e0msh2034afd928c4ef4p198d90jsn2c391457611f",
        "X-RapidAPI-Host": "numbersapi.p.rapidapi.com"
    }

    response = requests.request("GET", maturl, headers=headers, params=querystring)

    json_data = json.loads(response.text)
    await ctx.send(f"Number: {json_data['number']}\nFact: {json_data['text']}")


@client.command()
async def translate(ctx):
    try:
        await ctx.send("Enter text:")

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        msg = await client.wait_for("message", check=check)

        turl = "https://google-translate1.p.rapidapi.com/language/translate/v2"

        payload = f"q={str(msg.content)}&target=bn&source=en"
        headers = {
            "content-type": "application/x-www-form-urlencoded",
            "Accept-Encoding": "application/gzip",
            "X-RapidAPI-Key": "38a88804e0msh2034afd928c4ef4p198d90jsn2c391457611f",
            "X-RapidAPI-Host": "google-translate1.p.rapidapi.com"
        }

        response = requests.request("POST", turl, data=payload, headers=headers)

        json_data = json.loads(response.text)
        await ctx.send(f"Bangla: {json_data['data']['translations'][0]['translatedText']}")

    except:
        await ctx.send("Monthly Limit Crossed. Give me money to buy subscription.")


@client.command()
async def news(ctx):
    try:
        await ctx.send("Enter region/topic/keyword(keep it single word):")

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        msg = await client.wait_for("message", check=check)
        await ctx.send("How many news you want?")
        cnt = await client.wait_for("message", check=check)
        await ctx.send("Fetching.......")

        gnews = GNews(period='1d', max_results=int(cnt.content))

        ns = gnews.get_news(str(msg.content))

        for i in range(int(cnt.content)):
            await ctx.send(ns[i]['description'])
            await ctx.send(ns[i]['url'])
            await ctx.send("===================================================================")
    except:
        await ctx.send("Oh no! It might be a wrong input or not enough news.")


@client.command()
async def twitter(ctx):
    try:
        await ctx.send("Enter #Hashtag:")

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        ht = await client.wait_for("message", check=check)
        await ctx.send("Number of tweets:")
        n = await client.wait_for("message", check=check)
        url = "https://twitter154.p.rapidapi.com/hashtag/hashtag"

        querystring = {"hashtag": f"#{str(ht.content)}", "limit": f"{int(n.content)}", "section": "top"}

        headers = {
            "X-RapidAPI-Key": "38a88804e0msh2034afd928c4ef4p198d90jsn2c391457611f",
            "X-RapidAPI-Host": "twitter154.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        json_data = json.loads(response.text)
        print(json_data['results'][0])
    except:
        await ctx.send("Could not find!")


@client.command()
async def animePic(ctx):
    animeurl = "https://any-anime.p.rapidapi.com/anime/img"

    headers = {
        "X-RapidAPI-Key": "2acd06e12emshc3e71684876b746p1adf4djsn4e44ca270ab4",
        "X-RapidAPI-Host": "any-anime.p.rapidapi.com"
    }

    response = requests.request("GET", animeurl, headers=headers)

    print(response.text)


client.run(DISCORD_TOKEN)
