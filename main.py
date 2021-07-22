import urllib.request
import re
import discord
from discord.ext.commands import Bot
from keep_alive import keep_alive
import os
import requests
from bs4 import BeautifulSoup as bs

bot = Bot(command_prefix='?')
bot.remove_command("help")

def get_video(search_query):
    search_query = search_query.split()

    for i in range(4):
      search_query.pop(0)

    new_query = ""
    for i in range(len(search_query)):
      new_query = f"{new_query}{(search_query[i])}+"

    html = urllib.request.urlopen(f"https://www.youtube.com/results?search_query={new_query}") # Downloading YouTube Search Page HTML Content
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode()) # Finds the video IDs on the search page

    return f"https://www.youtube.com/watch?v={video_ids[0]}"

def get_wiki(search_query):
  search_query = search_query.split()

  for i in range(5):
    search_query.pop(0)
  
  if search_query[0] == "a" or search_query[0] == "an" or search_query[0] == "the" or search_query[0] == "who":
    search_query.pop(0)
  if search_query[len(search_query) - 1] == "are" or search_query[len(search_query) - 1] == "is" or search_query[len(search_query) - 1] == "were" or search_query[len(search_query) - 1] == "was":
    search_query.pop(len(search_query) - 1)

  new_query = ""

  for i in range(len(search_query)):
    new_query = f"{new_query}{(search_query[i])}"
    if i != len(search_query):
      new_query = f"{new_query}_"

  url = f"https://en.wikipedia.org/wiki/{new_query}"
  response = requests.get(url)
  # Extracting raw HTML content from page
  soup = bs(response.content, "html.parser")
  # Looking for text saying "This is not a valid article"
  isValid = soup.find("b", text="Wikipedia does not have an article with this exact name.")
  if isValid != None: # Checking if it is a valid article
    return False
  else:
    return f"https://en.wikipedia.org/wiki/{new_query}"

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.lower().startswith("i wish i knew how to"):
      url = get_video(message.content.lower())
      await message.channel.send(f"<@{message.author.id}>, Your wish is granted! {url}")
    elif message.content.lower().startswith("i wish i knew"):
      url = get_wiki(message.content.lower())
      if url == False:
        return
      else:
        await message.channel.send(f"<@{message.author.id}>, Your wish is granted! {url}")

@bot.event
async def on_ready():
  print('We have logged in as {0.user}'.format(bot))
  await bot.change_presence(activity=discord.Game('E.T. on Atari'))

keep_alive()
bot.run(os.getenv('TOKEN'))