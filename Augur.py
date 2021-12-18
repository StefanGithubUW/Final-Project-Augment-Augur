import discord
import tftfunctions

client = discord.Client()

profile = {'hes': False, 'gt': False, 'lvl': 1}

augurCommands = {
    '$Help': "Displays information about available commands!",
    '$Augur': "Starts an instance of the Augment Augur Program!",
    '$Roll X': "You can see how many rolls you can expect from your gold by entering the"
               "command $roll X, with X being the amount of gold you wish to roll! If you"
               "have the Golden Ticket Augment, this will provide you with an estimated roll count",
    '$Profile': "Displays information about available commands, or a command in specific!",
    '$Add X': "Adds an element to your Profile. You can replace X with Golden Ticket or High End Shopping "
              "to add augments, or you can replace it with level (or lvl) to increase your level by one",
    'Remove X': "Removes an element to your Profile. You can replace X with Golden Ticket or High End Shopping "
                "to remove augments, or you can replace it with level (or lvl) to remove your level by one",
    '$Set Level X': "Sets your level to the value you input for X, as long as it is between 1 and 10",
    '$Find X': "Calculates statistics about your ability to find a unit, with X being the name of the unit"

}


def yesorno(userinput):
    if userinput[0].lower() == 'y' or userinput[0] == 1:
        return "y"
    else:
        return "n"


async def sendemb(message, title="Title", url=None, description="description", color=0xFF5733):
    if url != None:
        embed = discord.Embed(title=title, url=url, description=description, color=color)
    else:
        embed = discord.Embed(title=title, description=description, color=color)

    await message.channel.send(embed=embed)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    # If the bot sent the message, nothing happens
    if message.author == client.user:
        return

    content = message.content.lower()

    if content.startswith("embed"):
        await sendemb(message)

    # returns true if the bot is by the same author as the one to send the
    # first message
    def check(msg):
        return msg.author == message.author and msg.channel == message.channel

    if content.startswith('$augur') or content.startswith("$new"):
        profile['hes'] = False
        profile['gt'] = False
        profile['lvl'] = 1
        await sendemb(message, title="Starting New Profile", description="Your augments and level have been reset! "
                                                                         "To see supported commands, Enter $Help")

    if content.startswith("$help"):
        helpmessage = ""
        for command in augurCommands:
            helpmessage += '%s: %s\n\n' % (command, augurCommands[command])

        await sendemb(message, title="$Help Command Received", description=helpmessage)

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

    if content.startswith('$profile'):
        profmessage = ""
        # for item in profile:
        #     profmessage += "%s: %s\n"%(item, profile[item])

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

    if content.startswith("$set level") or content.startswith("$set lvl"):
        cont = content.split()
        toset = int(cont[2])

        if toset > 0 and toset < 11:
            profile['lvl'] = toset

            await sendemb(message, title="Level Adjusted", description="You Are Now Level %s" % (profile['lvl']))
        else:
            sendemb(message, title="Level Could Not Be Adjusted",
                    description="You Must Choose a Level Between 1 and 10")

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


client.run('OTE3NjU5NTQ1Nzc2NTc0NDk0.Ya77DQ.JWq8znvza_Ocufp_MXoAg4S14ow')
