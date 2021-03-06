import discord
import os
from stay_awake import stay_awake

bot = discord.Client()

@bot.event
async def on_ready():
  print("We have logged on as {0.user}".format(bot))

@bot.event
async def on_message(message):
  print("Received message")
  if message.author == bot.user:
    return
  
  if message.content.startswith("!standup"):
    await message.channel.send("Here is the standup message")
  

stay_awake()
bot.run(os.getenv('TOKEN'))