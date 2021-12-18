import discord
# def main():
#     print("Hello!")
#     info()
# level = 0
# cost = None
# gt = False
client = discord.Client()


async def info(message):
    await message.channel.send('Reached lvl')
    level = await client.wait_for('message')
    await message.channel.send('Reached special')
    special = await client.wait_for('message')
    if special.lower() == 'hes':
        level = level + 1
        gt = False
    elif special.lower() == 'gt':
        gt = True
    elif special.lower() == 'both':
        level += 1
        gt = True
    else:
        gt = False
    # cost = int(input("What Cost is Your Unit? "))
    con = await client.wait_for('message')
    if con == '1' or con == '2' or con == '3' or con == '4' or con == '5':
        cost = con
    else:
        cost = nametocost(con)
    if cost == "?":
        costcheck()

    copiesout = int(await client.wait_for('message'))
    othersout = int(await client.wait_for('message'))

    runcalculations(level, cost, gt, copiesout, othersout,)

# async def findfirst(message):
#     await message.channel.send('Input First Value')
#     firstval = await client.wait_for('message')
#     await message.channel.send(firstval.content)
#     secondval = secondvalu(message)
#     vallist = [firstval.content, secondval.content]
#     return vallist
#
#
# async def secondvalu(message):
#     await message.channel.send('Input Second Value')
#     secondval = await client.wait_for('message')
#     return secondval


def runcalculations(level, cost, gt = False, copiesout = 0, othersout = 0):

    finalop = []
    currentcopies = copiesinpool(cost, copiesout)
    finalop.append('Current Copies: %s' %(currentcopies))

    poolsize = totalpool(cost, othersout + currentcopies)
    finalop.append('Total Pool: %s'%(poolsize))

    curroddsbycost = oddsbycost(cost, level)
    finalop.append('Current Odds of Tier: %s'%(curroddsbycost))

    curroddsofhitting = oddsofhitting(cost, curroddsbycost, copiesout, othersout)
    finalop.append('Odds to Hit: %s'%(curroddsofhitting))

    attempts = round(attemptstohit(curroddsofhitting))
    if attempts != 0:
        finalop.append('Attempts to hit: %s'%(attempts))
    else:
        finalop.append('Attempts to hit: Not Applicable')

    gth = round(goldtohit(cost, attempts, gt))
    if gth != 0:
        finalop.append('Gold to hit: %s'%(gth))
    else:
        finalop.append('Gold to hit: Not Applicable')


    return finalop

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

# Returns the number of complete rolls left in an amount of gold
def absrollsremaining(gold):
    if (gold % 2) == 0:
        return (gold / 2)
    else:
        gold -= 1
        return (gold / 2)

# Returns the amount of a unit given a cost
def copiesinpool(cost, copiesout = 0):
    if cost == 1:
        copies = 29
    elif cost == 2:
        copies = 22
    elif cost == 3:
        copies = 18
    elif cost == 4:
        copies = 12
    else:
        copies = 10

    copiesinpool = copies - copiesout

    if copiesinpool < 0:
        copiesinpool = 0

    return copiesinpool

# Returns the total units of a cost in the pool
def totalpool(cost, othersout = 0):
    if cost == 1:
        totalpool = 377
    elif cost == 2:
        totalpool = 286
    elif cost == 3:
        totalpool = 234
    elif cost == 4:
        totalpool = 132
    else:
        totalpool = 80

    totalpool = totalpool - othersout

    if totalpool < 0:
        totalpool = 0

    return totalpool

# List of odds by level by cost
onecostodds = [0,1.00,1.00,0.75,0.55,0.45,0.25,0.19,0.15,0.10]
twocostodds = [0, 0.00,0.00,0.25,0.30,0.33,0.40,0.30,0.20,0.15]
threecostodds = [0,0.00,0.00,0.00,0.15,0.20,0.30,0.35,0.35,0.30]
fourcostodds = [0,0.00,0.00,0.00,0.00,0.02,0.05,0.15,0.25,0.30]
fivecostodds = [0,0.00,0.00,0.00,0.00,0.00,0.00,0.01,0.05,0.15]

# Finds the odds of a unit occupying a shop slot by cost
# according to the user's level
def oddsbycost(cost, level):
    if cost == 1:
        return onecostodds[level]
    elif cost == 2:
        return twocostodds[level]
    elif cost == 3:
        return threecostodds[level]
    elif cost == 4:
        return fourcostodds[level]
    else:
        return fivecostodds[level]

# Finds the likelihood a unit will show up in a roll of the shop
def oddsofhitting(cost, oddsofcost, copiesout = 0, othersout = 0, name = None):
    # add a if cost = None, find cost by name

    copies = copiesinpool(cost, copiesout)
    poolsize = totalpool(cost, othersout)
    unitoddsatcost = (copies/poolsize)
    # oddsofcost = oddsbycost(cost, level)

    # This formula ignores that odds will decrease if more than one
    # copies are in the shop, because I only want the odds to hit one
    if oddsofcost == None:
        return 0
    else:
        oddsofhitting = (oddsofcost*unitoddsatcost)*5
    # print("Odds to hit on one roll: %s" %(oddsofhitting))
    return oddsofhitting
    attemptstohit(oddsofhitting)

# calculates the amount of rolls needed to see a unit in shop
def attemptstohit(oddsofhitting):
    if oddsofhitting != 0:
        attemptstohit = (1.0000000/oddsofhitting)
    else: return 0
    # print("Attempts to hit: %s"%(attemptstohit))
    return attemptstohit

# Calculates the rolls that can be expected from golden ticket
# Either gold or rolls must be input
def goldenticketrollcalc(rolls = None, gold = None):
    if rolls == None:
        rolls = absrollsremaining(gold)

    ticketrolls = rolls * 0.35

    while ticketrolls >= 1:
        rolls += ticketrolls
        ticketrolls = ticketrolls * 0.35

    # print("Expected Rolls: %s"%(rolls))
    return rolls

# Finds the gold equivalent of a certain number of rolls
# with golden ticket
def gtgoldtohit(neededrolls):
    rolls = 0

    while rolls < neededrolls:
        rolls += 1
        gtrolls = goldenticketrollcalc(rolls)
        if gtrolls > neededrolls:
            return rolls

# Finds the needed gold to hit a unit in shop
def goldtohit(cost, attempts, gt = False, copiesout = 0, othersout = 0,):
    # oddsofhitting = 0.00909090909

    if attempts != 0:
        if gt == False:
            gth = attempts * 2
        else:
            gth = gtgoldtohit(attempts) * 2
    else: return 0
    return gth

onecostnames = ['caitlyn','camille','darius','ezreal','garen','graves','illaoi','kassadin','poppy','singed','twisted fate','twitch','ziggs']
twocostnames = ['blitzcrank','katarina','kogmaw','lulu','quinn','swain','talon','tristana','trundle','vi','warwick','zilean','zyra']
threecostnames = ['chogath','ekko','gangplank','heimerdinger','leona','lissandra','malzahar','miss fortune','samira','shaco','taric','vex','zac']
fourcostnames = ['braum','dr mundo','fiora','janna','jhin','lux','orianna','seraphine','sion','urgot','yone']
fivecostnames = ['akali','galio','jayce','jinx','kaisa','tahm kench','viktor','yuumi']

def nametocost(name):
    name = name.lower()
    if name in onecostnames:
        cost = 1
    elif name in twocostnames:
        cost = 2
    elif name in threecostnames:
        cost = 3
    elif name in fourcostnames:
        cost = 4
    elif name in fivecostnames:
        cost = 5
    else:
        cost = '?'

    return cost

def costcheck():
    con = input("Enter Cost or Name? ")
    if con == 1 or con == 2 or con == 3 or con == 4 or con == 5:
        cost = con
    else:
        cost = nametocost(con)
    if cost == "?":
        costcheck()

# info()