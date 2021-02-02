import discord
from discord.utils import get
import json

with open('./env.json') as f:
  jData = json.load(f)

client = discord.Client()

@client.event
async def on_ready():
    print(f"worshipping mango as {client.user}")

@client.event
async def on_message(message):
    print("---------- NEW MESSAGE ----------")
    print("Channel: " + str(message.channel))
    print("User: " + str(message.author))
    print("Content: " + str(message.content))

    ################
    #              #
    # n00b handler #
    #              #
    ################

    # Add new users to the n00b role. Based on server event messages in #welcome because on_member_join wasn't working
    if str(message.channel) == "welcome":
        member = message.author
        print(f"User {member} joined the server")
        roleGuild = get(member.guild.roles, name="n00b")
        await member.add_roles(roleGuild)

    # Once user accepts the rules and declares major, they are released from n00b and added to the respective major
    if str(message.channel) == "start-here":
        if not message.content.startswith("!no-delete"): # Allows for messages in this channel to not get deleted
            # EE
            if message.content.upper() == "EE":
                member = message.author
                print(f"Adding EE to {member}")
                roleGuild = get(member.guild.roles, name="EE")
                await member.add_roles(roleGuild)
                roleGuild = get(member.guild.roles, name="n00b")
                await member.remove_roles(roleGuild)
            await message.delete()

    # ignore messages from the bot
    if message.author == client.user:
        print("Bot message. Ignoring own mango worship.")
        return

    # Hello!
    if message.content.startswith("!hello"):
        await message.channel.send("Hello!")

    # Echo the message sent
    if message.content.startswith("!echo"):
        response = message.content
        response = response.replace('!echo ', '')
        response = response.split(",")
        for x in response:
            await message.channel.send(x)


    #################
    #               #
    # Role commands #
    #               #
    #################

    # add roles
    if message.content.startswith("!add-role"):
        # check if user provided roles
        if ((message.content == "!add-role") or (message.content == "!add-roles")):
            await message.channel.send("The mango council will only consider filled out applications.")
            return

        member = message.author

        roles = message.content
        roles = roles.replace('!add-role ', '')
        roles = roles.replace('!add-roles ', '')
        roles = roles.split(",")

        for r in roles:
            roleGuild = get(member.guild.roles, name=r.upper())
            if type(roleGuild) == discord.role.Role:
                await member.add_roles(roleGuild)
                await message.channel.send(f"Your mango bretheren in \"{r.upper()}\" welcome you.")
            else:
                await message.channel.send(f"The mango council is too busy for this; \"{r}\" doesn't exist!")

    # remove roles
    if message.content.startswith("!rm-role"):
        # check if user provided roles
        if ((message.content == "!rm-role") or (message.content == "!rm-roles")):
            await message.channel.send("The mango council will only consider filled out applications.")
            return

        member = message.author

        roles = message.content
        roles = roles.replace('!rm-role ', '')
        roles = roles.replace('!rm-roles ', '')
        roles = roles.split(",")

        for r in roles:
            roleGuild = get(member.guild.roles, name=r.upper())
            if type(roleGuild) == discord.role.Role:
                await member.remove_roles(roleGuild)
                await message.channel.send(f"The mango council has revoked your membership in \"{r.upper()}\".")
            else:
                await message.channel.send(f"Stop wasting the Mango Council's time! \"{r}\" doesn't exist.")

    # little easter egg :)
    if message.content == "What's a sexy fruit?":
        await message.channel.send("Mango is really sexy. DON'T cut it up and eat it with a fork though. You have to let the juice drip down your face and onto your naked rack. You have to s-s-s-suck on that seed. Share it visually and expressively and then literally. Nothing, nothing better than a beautiful, sweet mango smeared all over the body and slowly kissed and licked off.\n     -Spanky Gazpacho DW")

##################
#                #
#   Client run   #
# (change token) #
#                #
##################

client.run(jData["discordToken"])