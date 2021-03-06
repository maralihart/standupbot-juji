import discord
import os
from stay_awake import stay_awake

bot = discord.Client()

@bot.event
async def on_ready():
  print("We have logged on as {0.user}".format(bot))

@bot.event
async def on_message(message):

  if message.author == bot.user:
    return
  
  if message.content.startswith("!approve"):

    if len(message.mentions) == 0:
      await message.channel.send("No one was mentioned. Please try again.")

    for mention in message.mentions:
      try:
        await mention.send("You've been notified")
      except:
        await message.channel.send("Notification could not be sent.")

"""
Use case:
We have a new design
It needs to send approval to admin
But it needs to get sent to developers
Then developers approve and it goes back to admin
then design can get started
"""

stay_awake()
bot.run(os.getenv('TOKEN'))