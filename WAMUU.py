import os
import random
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('TOKEN')
GUILD = os.getenv('GUILD')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='WAMUU', intents=intents)

@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(f'{bot.user.name} has connected to Discord on server {guild}(id: {guild.id})')

awakenHelpText = '''Awakens the pillar men.\n
               Usage: WAMUU! (reason) (users)
               Both arguments are optional, but you have to include at least either argument i.e. arguments cannot be empty.\n
               Example usage:\n
               WAMUU! its time to play
               WAMUU! @Meor
               WAMUU! @Meor @Faiq
               WAMUU! its time to play @Meor @Faiq\n
               WAMUU! <= this by itself is a nono.'''
@bot.command(name='!', help=awakenHelpText)
async def awaken(ctx, *, args):
    newArgs = ''.join(args).split()
    hasReason = True
    if newArgs[0][0] == '<':
        hasReason = False

    hasUser = False
    for arg in newArgs:
        if arg[0] == '<':
            hasUser = True
            break

    wamuuQuote = [
        'The time has come. Awaken my masters',
        'AYAYAYAAAAA'
    ]
    wamuuGifLink = 'https://tenor.com/view/pillar-men-awaken-my-masters-awaken-jojos-bizarre-adventure-jjba-gif-19344086'
    response = random.choice(wamuuQuote)

    # if the arguments included a reason and at least one user
    if hasUser and hasReason:
        # concatening the reason string
        reason = ''
        userStartIdx = -1
        for i in range(len(newArgs)):
            if newArgs[i][0] != '<':
                if newArgs[i+1][0] != '<':
                    reason += newArgs[i] + ' '
                else:
                    reason += newArgs[i]
            else:
                userStartIdx = i
                break
        
        # putting all users into a list, and then removing duplicates
        users = []
        for i in range(userStartIdx, len(newArgs)):
            users.append(await commands.UserConverter().convert(ctx, newArgs[i]))
        users = list(dict.fromkeys(users))

        # concatening all users' name called
        
        names = ''
        for i in range(len(users)):
            if i == len(users)-1:
                names = names + f'{users[i].mention}***!***'
            else:
                names = names + f'{users[i].mention}***,*** '

        # then sends message to channel
        await ctx.send(f'***{response}*** {names}\n{reason}')
        await ctx.send(wamuuGifLink)

        # dming the users called
        for user in users:
            await user.send('***The time has come. Awaken my master!***')
            await user.send(reason)
            await user.send(wamuuGifLink)
    # if the arguments only included a reason
    elif not hasUser and hasReason:
        # joining the reason string
        reason = ' '.join(newArgs)

        # sending message to channel
        await ctx.send(f'***{response}!***\n{reason}')
        await ctx.send(wamuuGifLink)
    # if the arguments only included at least one user
    elif hasUser and not hasReason:
        # putting all users into a list, and then removing duplicates
        users = []
        for i in range(len(newArgs)):
            users.append(await commands.UserConverter().convert(ctx, newArgs[i]))
        users = list(dict.fromkeys(users))

        # concatening all users' name called
        names = ''
        for i in range(len(users)):
            if i == len(users)-1:
                names = names + f'{users[i].mention}***!***'
            else:
                names = names + f'{users[i].mention}***,*** '

        # then sends message to channel
        await ctx.send(f'***{response}*** {names}')
        await ctx.send(wamuuGifLink)

        # dming the users called
        for user in users:
            await user.send('***The time has come. Awaken my master!***')
            await user.send(wamuuGifLink)

@awaken.error
async def awakenError(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('You need to have a reason to wake the pillar men up or a pillar man to wake up.\nType WAMUUhelp ! for more details.')
        await ctx.send('https://tenor.com/view/anime-jotaro-jjba-jojo-yare-gif-12243323')
    else:
        await ctx.send('Something is wrong. Call Kars!')
        await ctx.send('https://tenor.com/view/jo-jos-bizarre-adventure-kars-flip-hair-gif-13789724')
        print(error)

bot.run(TOKEN)