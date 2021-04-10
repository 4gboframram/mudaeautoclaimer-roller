#imports
import discord
import asyncio
import json
import re
import time
from colorama import init
from termcolor import colored

Channels=open('channels.txt','r').read().splitlines() #channels config
characters=open('characters.txt','r').read().splitlines() #characters config
Series=open('series.txt','r').read().splitlines()
#load all config.json shit and create variables

config_file=open("config.json",'r')
config=json.load(config_file)

TOKEN = config["TOKEN"]
reactionDelay=config["reactionDelay"]
command=config["command"]
timeBetweenRolls=config["timeBetweenRolls"]
numberOfRolls=config["numberOfRolls"]
typingTime=config["typingTime"]
dkCommand=config["dkCommand"]
dailyCommand=config["dailyCommand"]
client=discord.Client() 

    

init() #initiate colorama for colors in the console
def search(string):
    
    temp = re.findall(r'\d+', string)
    res = list(map(int, temp)) #gives a list of all integers in a string 
    return res                   
    
async def doRollsInner(channel): #this function is an infinite loop
        chanel=client.get_channel(int(channel)) #I love mispelling on purpose
        name=chanel.name 
        await chanel.send(command)
        current_time = time.strftime("%D %H:%M:%S", time.localtime())
        print(colored(f"[{current_time}] Rolling in channel '{name}'","cyan"))
        norolls=False
        i=1
        while norolls==False: #guarentee Mudae sending the No Rolls left message.
            current_time = time.strftime("%D %H:%M:%S", time.localtime())
            print(colored(f"\t[{current_time}] Attempting roll {i} of {numberOfRolls} in channel: '{name}' ",'blue'))
            async for message in chanel.history(limit=2):

                if 'the roulette is limited to' in message.content and client.user.name in message.content and message.author.bot==True:
                    current_time = time.strftime("%D %H:%M:%S", time.localtime())
                    norolls=message.content
                    print(f"[{current_time}] No rolls left in '{name}', Sleeping in '{name}' for {search(norolls)[1]+1} minutes")
                    await asyncio.sleep((search(norolls)[1]+1)*60)
                    await doRollsInner(channel)  #start again after sleeping. Done asyncronously. 

            if norolls==False:
                async with chanel.typing():
                    await asyncio.sleep(typingTime)
                await chanel.send(command)
                await asyncio.sleep(timeBetweenRolls-typingTime)
                i+=1 #move on to next roll

async def doRolls():
    await asyncio.sleep(2*timeBetweenRolls)
    for future in asyncio.as_completed(map(doRollsInner, Channels)): #basically do rolls asyncronously
        result = await future #because they have different wait times

async def dailyClaim(channel):
    current_time = time.strftime("%D %H:%M:%S", time.localtime())
    chanel=client.get_channel(int(channel))
    print(colored(f"[{current_time}] Attempting to claim daily kakera in {chanel.name}",'magenta'))
    async with chanel.typing():
        await asyncio.sleep(typingTime)
    await chanel.send(f"{dkCommand}")
    await asyncio.sleep(timeBetweenRolls)
    async for message in chanel.history(limit=5): #in case other users busy rolling, make the limit higher
        if f"Next {dkCommand} reset" in message.content and message.author.bot==True:
            try:
                current_time = time.strftime("%D %H:%M:%S", time.localtime())
                t=search(message.content)
                if len(t)<=1: #basically if there's either only hours or only minutes
                                #idk if only hours is a thing, but just in case
                    if 'h' in message.content: 
                        print(colored(f"[{current_time}] Next {dkCommand} in '{chanel.name}' in {t[0]}h 0m. Asyncronously sleeping in '{chanel.name}' that amount of time.",'cyan'))
                        await asyncio.sleep(3600*t[0])
                    if 'min' in message.content: 
                        print(colored(f"[{current_time}] Next {dkCommand} in '{chanel.name}' in 0h {t[0]}m. Asyncronously sleeping in '{chanel.name}' that amount of time.",'cyan'))
                        await asyncio.sleep(60*t[0])
                print(colored(f"[{current_time}] Next {dkCommand} in '{chanel.name}' in {t[0]}h {t[1]}m. Asyncronously sleeping in '{chanel.name}' that amount of time.",'cyan'))
                await asyncio.sleep(3600*t[0]+60*t[1]+1) #first integer in the message is the hour, second integer is the minutes
                await dailyClaim(channel)
            except IndexError: continue #when search() doesn't return anything, ignore the error raised and try again

        else: #if daily claim fails due to Mudae being ratelimited or something, try again
            await asyncio.sleep(3*timeBetweenRolls-typingTime) 
            await dailyClaim(channel)
    await asyncio.sleep(timeBetweenRolls-typingTime)
   
async def doDailyClaim():
    for future in asyncio.as_completed(map(dailyClaim, Channels)): #basically do dk claiming asyncronously
        result = await future #because they have different wait times         

async def daily(channel):
    await asyncio.sleep(5*timeBetweenRolls-typingTime)
    current_time = time.strftime("%D %H:%M:%S", time.localtime())
    chanel=client.get_channel(int(channel))
    print(colored(f"[{current_time}] Attempting to claim {dailyCommand} in {chanel.name}",'magenta'))
    async with chanel.typing():
        await asyncio.sleep(typingTime)
    await chanel.send(f"{dailyCommand}")
    await asyncio.sleep(timeBetweenRolls)
    async for message in chanel.history(limit=5): #in case other users busy rolling, make the limit higher
        if f"Next {dailyCommand} reset" in message.content and message.author.bot==True:
            try:
                current_time = time.strftime("%D %H:%M:%S", time.localtime())
                t=search(message.content)
                if len(t)<=1: #basically if there's either only hours or only minutes
                                #idk if only hours is a thing, but just in case
                    if 'h' in message.content: 
                        print(colored(f"[{current_time}] Next {dailyCommand} in '{chanel.name}' in {t[0]}h 0m. Asyncronously sleeping in '{chanel.name}' that amount of time.",'cyan'))
                        await asyncio.sleep(3600*t[0])
                    if 'min' in message.content: 
                        print(colored(f"[{current_time}] Next {dailyCommand} in '{chanel.name}' in 0h {t[0]}m. Asyncronously sleeping in '{chanel.name}' that amount of time.",'cyan'))
                        await asyncio.sleep(60*t[0])
                print(colored(f"[{current_time}] Next {dailyCommand} in '{chanel.name}' in {t[0]}h {t[1]}m. Asyncronously sleeping in '{chanel.name}' that amount of time.",'cyan'))
                await asyncio.sleep(3600*t[0]+60*t[1]+1) #first integer in the message is the hour, second integer is the minutes
                await daily(channel)
            except IndexError: continue #when search() doesn't return anything, ignore the error raised and try again

        else: #if daily claim fails due to Mudae being ratelimited or something, try again
            await asyncio.sleep(3*timeBetweenRolls-typingTime) 
            await daily(channel)
    await asyncio.sleep(timeBetweenRolls-typingTime)
   
async def doDaily():
    for future in asyncio.as_completed(map(daily, Channels)): #basically do daily claiming asyncronously
        result = await future #because they have different wait times         

       
@client.event
async def on_ready(): 
    current_time = time.strftime("%D %H:%M:%S", time.localtime())
    print(colored(f'[{current_time}] Logged in as {client.user.name}','green'))
    await asyncio.gather(doRolls(), doDailyClaim(),doDaily()) #when user logs on, call doRolls(), doDailyClaim() and doDaily()

@client.event
async def on_message(message):
    if str(message.channel.id) not in Channels:
        return #return when a message is not in the user-provided list of channels
    
    #autoclaimer by name and series
    try:
        title=message.embeds[0].author.name
        description=message.embeds[0].description
        channelName=message.channel.name


        if title in characters or any(series in description for series in Series): 
            #mudae uses the author field for character names in its embeds.

            try:
               
                current_time = time.strftime("%D %H:%M:%S", time.localtime())
                print(colored(f"\n[{current_time}] Trying to claim: {str(title)}",'blue'))
                
                await asyncio.sleep(reactionDelay)
                try:
                    if '/' in message.embeds[0].footer.text: #if a character's image card is shown, say someone tried to fool the bot
                            current_time = time.strftime("%D %H:%M:%S", time.localtime()) #Only image cards contain a "/" in the footer.'
                                                                                          #The reason I don't only search to see if the footer exists 
                                                                                          #is because the 2 rolls left message is in the footer too by default
                            print(colored(f'[{current_time}] Someone tried to fool the bot in channel \'{channelName}\' by sending {title}\'s info card','yellow'))
                            return
                except TypeError: #There won't be a footer on normal sent characters or wishes
                    pass          #because empty embed fields are not iterable
                await message.add_reaction(message.reactions[0])
                current_time = time.strftime("%D %H:%M:%S", time.localtime())
                print(colored(f'\t[{current_time}] Reacted to {title} in channel \'{channelName}\' with ','blue')+colored(f'\'{message.reactions[0]}\'','cyan'))
                print(colored(f"\t[{current_time}] Probably claimed {title} in channel '{channelName}'",'green')+'\n\t The above could be a false positive if the if your claim timer is on cooldown.')
            
            except IndexError: #if no reactions

                try: 
                    await message.add_reaction("❤️")
                    current_time = time.strftime("%D %H:%M:%S", time.localtime())
                    print(colored(f"[{current_time}] \tProbably claimed {title} in channel '{channelName}'",'green', 'on_yellow')+'\n\tThe above could be a false positive if the list of wanted characters has the name of another user\'s harem name in it, or if your claim timer is on cooldown, \nor if somebody is searched for an image of the character you wanted')

                except Exception as e: #if anything goes wrong claiming by adding our own reaction, print the exception
                    current_time = time.strftime("%D %H:%M:%S", time.localtime())
                    print(colored(f'\t[{current_time}] Could not claim {title} in channel \'{channelName}\' because {e}', 'red'))
            except Exception as e: #if anything goes wrong claiming normally
                current_time = time.strftime("%D %H:%M:%S", time.localtime())
                print(colored(f'\t[{current_time}] Could not claim {title} in channel \'{channelName}\' because {e}', 'red'))

        else: #used so the user knows the program is reading the messages successfully.
            current_time = time.strftime("%D %H:%M:%S", time.localtime())
            print(colored(f"\n[{current_time}] Ignoring {title}, in channel '{channelName}' because they are not wanted",'yellow'))
    except IndexError: #This IndexError is used to return when there is no Embed
        return
        

    
client.run(TOKEN, bot=False) #if you are reading this, have a nice day OwO, 
                            #and you are probably better than me at this lmao  