import discord
import os
import re
from stay_awake import stay_awake

bot = discord.Client()
mention_pattern = re.compile(r"<@.*>", re.DOTALL)

@bot.event
async def on_ready():
  print("We have logged on as {0.user}".format(bot))

@bot.event
async def on_message(message):

  author = message.author
  if author == bot.user:
    return

  name = author.nick if author.nick else author.name
  
  # APPROVE
  if message.content.startswith("!request"):
    await request(author, message, name)
    await message.delete()

  # REVIEWER
  elif message.content.startswith("!reviewer"):
    await add_reviewer(author, message, name)
    await message.delete()

  # APPROVED
  elif message.content.startswith("!approve"):
    await approve(author, message, name)
    await message.delete()
    
def create_mention(id):
  return "<@"+str(id)+">"

async def request(author, message, name):

  global mention_pattern

  header = ":rotating_light:  **NEW APPROVAL REQUEST **:rotating_light: \n \n"

  edited_content = mention_pattern.sub(r"", message.content[8:].strip()).strip()

  if len(edited_content) == 0:
      await message.channel.send("No message was given. Please try again.")
      return

  if len(message.mentions) == 0:
    await message.channel.send("No one was mentioned. Please try again.")
    return

  else:
    to_mention = []
    for mention in message.mentions:
      to_mention.append(mention)
      try:
        await mention.send(header + "Please review this message from **" + name + "**: \n" + edited_content + "\n \nFor more information, please go to the **" + message.channel.name + "** channel in the server **" + message.guild.name + "**")

      except:
        await message.channel.send("Notification could not be sent to " + create_mention(mention.id) + ". Please ensure that they have their DM privileges on.")

    await message.channel.send(header + create_mention(author.id) + " requested approval from " + " ".join(create_mention(mention.id) for mention in to_mention) + ": \n" + edited_content)

async def add_reviewer(author, message, name):
  global mention_pattern

  header = ":bangbang:  **NEW REVIEWER ADDED **:bangbang: \n \n"

  edited_content = mention_pattern.sub(r"", message.content[10:].strip()).strip()

  message_link_pattern = re.compile(r"https://discord.com/channels/[0-9]+/[0-9]+/[0-9]+", re.DOTALL)
  og_message_link = re.findall(message_link_pattern, message.content)

  edited_content = message_link_pattern.sub(r"", edited_content).strip()

  if len(og_message_link) == 1:
    og_message = await message.channel.fetch_message(''.join(og_message_link)[67:])

  else:
    await message.channel.send("Please be sure to link one message. Please try again.")
    return

  if len(message.mentions) == 0:
      await message.channel.send("No one was mentioned. Please try again.")
      return

  else:
    to_mention = []
    for mention in message.mentions:
      to_mention.append(mention)
      try:
        await mention.send(header + "You've been added as a reviewer by **" + name + "**: \n" + edited_content + "\n \nFor more information, please go to " + og_message_link)

      except:
        await message.channel.send("Notification could not be sent to " + create_mention(mention.id) + ". Please ensure that they have their DM privileges on.")

    await message.channel.send(header + create_mention(author.id) + " added " + " ".join(create_mention(mention.id) for mention in to_mention) + " as reviewers \n" + edited_content + "\n \n**Original Message**: " + og_message.content[62:] + "\n \n" + "To see original request message, please go here " + ''.join(og_message_link))

async def approve(author, message, name):
  global mention_pattern

  header = ":white_check_mark:  **REQUEST APPROVED **:white_check_mark: \n \n"

  message_link_pattern = re.compile(r"https://discord.com/channels/[0-9]+/[0-9]+/[0-9]+", re.DOTALL)
  og_message_link = re.findall(message_link_pattern, message.content)

  if len(og_message_link) == 1:
    og_message = await message.channel.fetch_message(''.join(og_message_link)[67:])

    og_author_pattern = re.compile(r"\n.*requested", re.DOTALL)
    og_author = ''.join(re.findall(og_author_pattern, og_message.content))
    og_author_id = og_author[og_author.find("<@")+2:og_author.find("> requested")]
    og_author = await bot.fetch_user(og_author_id)

  else:
    await message.channel.send("Please be sure to link one message. Please try again.")
    return

  try:
    await og_author.send(header + "*Original Message: \n" + og_message.content[62:] + "\n \nFor more information, please go to " + og_message_link)

  except:
    await message.channel.send("Notification could not be sent to " + create_mention(og_author.id) + ". Please ensure that they have their DM privileges on.")

  await message.channel.send(header + create_mention(author.id) + " approved the following message from " + create_mention(og_author_id) +" :arrow_down: " + og_message.content[62:] + "\n \n" + "To see original request message, please go here " + ''.join(og_message_link))

stay_awake()
bot.run(os.getenv('TOKEN'))