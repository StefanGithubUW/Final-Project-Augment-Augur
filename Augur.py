import discord
import tftfunctions

client = discord.Client()

# This is the basic profile, which shows the important info about the current user's game state
profile = {'hes': False, 'gt': False, 'lvl': 1}

# Dictionary of commands the bot accepts, in a command: description format
augurCommands = {
    '$Help': "Displays information about available commands!",
    '$Augur': "Starts an instance of the Augment Augur Program!",
    '$Roll X': "You can see how many rolls you can expect from your gold by entering the"
               "command $roll X, with X being the amount of gold you wish to roll! If you"
               "have the Golden Ticket Augment, this will provide you with an estimated roll count",
    '$Profile': "Displays information about available commands, or a command in specific!",
    '$Add X': "Adds an element to your Profile. You can replace X with Golden Ticket or High End Shopping "
              "to add augments, or you can replace it with level (or lvl) to increase your level by one",
    'Remove X': "Removes an element from your Profile. You can replace X with Golden Ticket or High End Shopping "
                "to remove augments, or you can replace it with level (or lvl) to remove your level by one",
    '$Set Level X': "Sets your level to the value you input for X, as long as it is between 1 and 10",
    '$Find X': "Calculates statistics about your ability to find a unit, with X being the name of the unit"
}

# This utility method sends a message to the discord client in the form of an "Embed". It is in
# this format to show that it is from the bot, and to keep output organized
async def sendemb(message, title="Title", url=None, description="description", color=0xFF5733):

    # Formats the embed based on passed in parameters
    if url != None:
        embed = discord.Embed(title=title, url=url, description=description, color=color)
    else:
        embed = discord.Embed(title=title, description=description, color=color)

    # Sends the embed to the discord client
    await message.channel.send(embed=embed)


# When the program connects to discord and is ready to perform actions
# it triggers the on_ready event
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


# Whenever a message is sent, it triggers the on_message event and passes in
# the message object as a parameter. This is used to collect commands
@client.event
async def on_message(message):
    # If the bot sent the message, nothing happens
    if message.author == client.user:
        return

    content = message.content.lower()

    # Command for the bot to start tracking a new set of info,
    # not case-sensitive.
    if content.startswith('$augur') or content.startswith("$new"):
        profile['hes'] = False
        profile['gt'] = False
        profile['lvl'] = 1
        await sendemb(message, title="Starting New Profile", description="Your augments and level have been reset! "
                                                                         "To see supported commands, Enter $Help")

    # Command for the bot to output a help message to the client
    if content.startswith("$help"):
        helpmessage = ""
        for command in augurCommands:
            helpmessage += '%s: %s\n\n' % (command, augurCommands[command])

        await sendemb(message, title="$Help Command Received", description=helpmessage)

    # Command for the Bot to find the number of rolls possible with
    # a given amount of gold. Command is input with the format $roll X,
    # where X is an integer value. The command is not caps sensitive.
    # In the case that the user has the Golden Ticket augment, each roll
    # will have a 35% chance to grant another roll. Free rolls provided by
    # the augment are also subject to this chance. Command is not case-sensitive
    if content.startswith('$roll'):
        if profile['gt'] == False:
            gold = message.content[6:]
            gold = int(gold)
            rollsrem = tftfunctions.rollsremaining(gold)
            rolltitle = ""
            rollvals = ""
            rolltitle = "Calculating Rolls With %s Gold" % (gold)
            rollvals = "Rolls: %s" % (rollsrem)
            await sendemb(message, title=rolltitle, description=rollvals)
        else:
            gold = message.content[6:]
            gold = int(gold)
            rolltitle = ""
            rollvals = ""
            rolltitle = "Calculating Rolls With %s Gold and Golden Ticket Active" % (gold)
            rollsexpected = tftfunctions.goldenticketrollcalc(gold=gold)
            rollvals = "Expected Rolls: %s" % (round(rollsexpected, 2))
            await sendemb(message, title=rolltitle, description=rollvals)

    # Command to output user's game info to the discord client
    # The command is not case-sensitive.
    if content.startswith('$profile'):
        profmessage = ""

        profmessage += "You are Level %s\n" % (profile['lvl'])
        if profile['hes']:
            profmessage += "You have the High End Shopping Augment!\n"
            if profile['gt']:
                profmessage += "You have the Golden Ticket Augment!"
        else:
            if profile['gt']:
                profmessage += "You have the Golden Ticket Augment!"
            else:
                profmessage += "No Active Augment Modifiers"
        await sendemb(message, title="Current Profile", description=profmessage)

    # Commands to add an element to the Profile: This can be one of the two augments
    # with an economic/roll chance impact, or an increase to level (level cannot go above 10)
    # The commands are not case-sensitive.
    if content.startswith("$add hes") or content.startswith('$add high end shopping'):
        profile['hes'] = True
        await sendemb(message, title="Profile Adjusted", description="High End Shopping Augment Acquired")
    elif content.startswith("$add gt") or content.startswith('$add golden ticket'):
        profile['gt'] = True
        await sendemb(message, title="Profile Adjusted", description="Golden Ticket Augment Acquired")
    elif content.startswith("$add level") or content.startswith('$add lvl') \
            or content.startswith("$levelup") or content.startswith('$level up'):
        if profile['lvl'] != 10:
            profile["lvl"] += 1
            await sendemb(message, title="Level Adjusted", description="You Are Now Level %s" % (profile['lvl']))
        else:
            await sendemb(message, title="Level Could Not Be Changed", description="Levels Cannot Go Above 10")

    # Commands to remove an element from the Profile: This can be one of the two augments
    # with an economic/roll chance impact, or an decrease to level (level cannot go below 1)
    # The commands are not case-sensitive.
    if content.startswith("$remove hes") or content.startswith('$remove high end shopping'):
        profile['hes'] = False
        await sendemb(message, title="Profile Adjusted", description="High End Shopping Augment Removed")
    elif content.startswith("$remove gt") or content.startswith('$remove golden ticket'):
        profile['gt'] = False
        await sendemb(message, title="Profile Adjusted", description="Golden Ticket Augment Removed")
    elif content.startswith("$remove level") or content.startswith('$remove lvl'):
        if profile['lvl'] != 1:
            profile["lvl"] -= 1
            await sendemb(message, title="Level Adjusted", description="You Are Now Level %s" % (profile['lvl']))
        else:
            await sendemb(message, title="Level Could Not Be Changed", description="Levels Cannot Go Below 1")

    # An alternative to adding/removing levels, this sets your level to a desired value
    # between 1 and 10. The command is not case-sensitive.
    if content.startswith("$set level") or content.startswith("$set lvl"):
        cont = content.split()
        toset = int(cont[2])

        if toset > 0 and toset < 11:
            profile['lvl'] = toset

            await sendemb(message, title="Level Adjusted", description="You Are Now Level %s" % (profile['lvl']))
        else:
            sendemb(message, title="Level Could Not Be Adjusted",
                    description="You Must Choose a Level Between 1 and 10")

    # Command to find the odds of seeing a unit when consuming a roll,
    # The central component of the application. The desired unit must
    # exist in the current TFT game, and the command is not Case-Sensitive.
    # Not all units can be found at every level.
    if content.startswith('$find'):
        findx = message.content
        findxlist = findx.split()
        tofind = findxlist[1]

        cost = tftfunctions.nametocost(tofind)

        if cost != "?":
            await sendemb(message, title="Finding Likelihood of %s: %s Cost" % (tofind, cost), description=
                                         "Please submit the number of copies of the unit in play and the number of "
                                         "other copies of units of the same cost, separated by a space")

            pool = await client.wait_for("message")
            pl = pool.content
            poollist = pl.split()
            copiesout = int(poollist[0])
            othersout = int(poollist[1])

            if not profile['hes']:
                toprint = tftfunctions.runcalculations(profile['lvl'], cost, profile['gt'], copiesout, othersout)
            else:
                toprint = tftfunctions.runcalculations(profile['lvl'] + 1, cost, profile['gt'], copiesout, othersout)

            calcs = ""
            for item in toprint:
                calcs += item
                calcs += "\n"

            await sendemb(message, title="To Find %s" % (tofind), description=calcs)


        else:
            await sendemb(message, title="That is Not a Valid Unit", description="Try checking your spelling")

import augurkey as augurkey
client.run(augurkey.key)
