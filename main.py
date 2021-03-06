import discord
import os
import re
from stay_awake import stay_awake

bot = discord.Client()
header = ":rotating_light:  **NEW APPROVAL REQUEST **:rotating_light: \n \n"

@bot.event
async def on_ready():
  print("We have logged on as {0.user}".format(bot))

@bot.event
async def on_message(message):
  global header

  author = message.author

  if author == bot.user:
    return
  
  if message.content.startswith("!approve"):

    name = author.nick if author.nick else author.name

    if len(message.mentions) == 0:
      await message.channel.send("No one was mentioned. Please try again.")

    for mention in message.mentions:
      try:
        mention_pattern = re.compile(r"<@.*>", re.DOTALL)
        edited_content = mention_pattern.sub(r"", message.content[8:].strip()).strip()

        await mention.send(header + "Please review this message from **" + name + "**: \n" + edited_content)

        await message.channel.send(header + "From " + create_mention(author.id) + " to " + create_mention(mention.id) + ": \n" + edited_content)

        

        await message.delete()

      except:
        await message.channel.send("Notification could not be sent.")
    
def create_mention(id):
  return "<@"+str(id)+">"
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