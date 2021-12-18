import discord

client = discord.Client()
def yesorno(userinput):
    if userinput[0].lower() == 'y' or userinput[0] == 1:
        return "y"
    else:
        return "n"

# This finds the rolls left for a certain amount of gold
def rollsremaining(gold, remainder = True):
    if remainder == True:
        if (gold % 2) == 0:
            return "Rolls: %s, Remainder: 0g."%(gold/2)
        else:
            gold -= 1
            return "Rolls: %s, Remainder: 1g." % (gold / 2)
    else:
        return "Rolls: %s" % (gold/2)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    c = message.channel

    def check(msg):
        return msg.author == message.author and msg.channel == message.channel and \
        msg.content.lower() in ["rolls", "rollsto"]

    if message.content.startswith('!help'):
        await c.send('Ready to Start a New Session?')
        await c.send('Want to Calculate Rolls? Type ROLLS, or type ROLLSTO to find a champ')


    if message.content.startswith('ROLLS'):
        # await c.send("How much gold do you have?")
        # cgold = await client.wait_for('gold')
        # cgold = int(cgold)
        # await c.send(cgold)
        # await c.send("Do you have Golden Ticket")
        # gtuinput = await client.wait_for('gt')
        # gtuinput = yesorno(gtuinput)
        #
        # # cgold = 32
        # # gtuinput = 'y'
        #
        #
        # if gtuinput == "y":
        #    await c.send(rollsremaining(cgold))
        await findrolls(c)

@client.event
async def findrolls(c):
    await c.send("How much gold do you have?")
    cgold = await client.wait_for('gold')
    cgold = int(cgold)
    await c.send(cgold)
    await c.send("Do you have Golden Ticket")
    gtuinput = await client.wait_for('gt')
    gtuinput = yesorno(gtuinput)

    if gtuinput == "y":
        await c.send(rollsremaining(cgold))

client.run('OTE3NjU5NTQ1Nzc2NTc0NDk0.Ya77DQ.JWq8znvza_Ocufp_MXoAg4S14ow')
