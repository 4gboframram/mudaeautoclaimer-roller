#imports
import discord
import asyncio
import json
import re
from time import sleep
from colorama import init
from termcolor import colored

Channels=open('Channels.txt','r').read().splitlines() #channels config
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

client=discord.Client() 

init() #initiate colorama for colors in the console
def search(string):
    
    temp = re.findall(r'\d+', string)
    res = list(map(int, temp)) #gives the number of minutes left. 
    return res                    #[0] is max number of rolls, which I may incorporate in the future
    

async def doRollsInner(channel): #this function is an infinite loop
        chanel=client.get_channel(int(channel)) #I love mispelling on purpose
        name=chanel.name 
        await chanel.send(command)
        print(colored(f"Excecuting task: Rolling in channel '{name}'","cyan"))
        norolls=False
        i=1
        while norolls==False: #guarentee Mudae sending the No Rolls left message.
            print(colored(f"\tAttempting roll {i} of {numberOfRolls} in channel: '{name}' ",'blue'))
            async for message in chanel.history(limit=2):

                if 'the roulette is limited to' in message.content and client.user.name in message.content and message.author.bot==True:
                    
                    norolls=message.content
                    print(f"No rolls left in '{name}', Sleeping in '{name}' for {search(norolls)[1]+1} minutes")
                    await asyncio.sleep((search(norolls)[1]+1)*60)
                    await doRollsInner(channel)  #start again after sleeping. Done asyncronously. 

            if norolls==False:
                async with chanel.typing():
                    await asyncio.sleep(typingTime)
                await chanel.send(command)
                await asyncio.sleep(timeBetweenRolls-typingTime)
                i+=1 #move on to next roll

async def doRolls():
    for future in asyncio.as_completed(map(doRollsInner, Channels)): #basically do rolls asyncronously
        result = await future #because they have different wait times

async def dailyClaim(channel):
    chanel=client.get_channel(int(channel))
    print(colored(f"Attempting to claim daily kakera in {chanel.name}",'magenta'))
    await asyncio.sleep(timeBetweenRolls-typingTime)
    async with chanel.typing():
        await asyncio.sleep(typingTime)
    await chanel.send("$dk")

    async for message in chanel.history(limit=5): #in case other users busy rolling, make the limit higher
        if "Next $dk reset" in message.content and message.author.bot==True:
            print(colored(f"Next $dk in {search(message.content)[0]}h {search(message.content)[1]}m. Asyncronously sleeping in '{chanel.name}' that amount of time.",'yellow'))
            await asyncio.sleep(3600*search(message.content)[0]+(search(message.content)[1]+1)*60) #first integer in the message is the hour, second integer is the minutes
            await dailyClaim(channel)
        else: #if daily claim fails do to Mudae being ratelimited or something, try again
            await asyncio.sleep(timeBetweenRolls-typingTime) 
            await dailyClaim(channel)
    await asyncio.sleep(timeBetweenRolls-typingTime)
   
async def doDailyClaim():
    for future in asyncio.as_completed(map(dailyClaim, Channels)): #basically do dk claiming asyncronously
        result = await future #because they have different wait times         

       
@client.event
async def on_ready(): 
    print(colored(f'Logged in as {client.user.name}','green'))
    await asyncio.gather(doRolls(), doDailyClaim()) #when user logs on, call doRolls and claimDaily)

@client.event
async def on_message(message):
    if str(message.channel.id) not in Channels:
        return #return when a message is not in the user-provided list of channels
    
    #autoclaimer by name
    try:
        title=message.embeds[0].author.name
        description=message.embeds[0].description
        if title in characters or any(series in description for series in Series): 
            #mudae uses the author field for character names in its embeds.

            try:
                print(colored(f"\n Trying to claim: {str(title)}",'blue'))
                await asyncio.sleep(reactionDelay)
                await message.add_reaction(message.reactions[0])
                print(colored(f'\tReacted to {title} with ','blue')+colored(message.reactions[0],'cyan'))
                print(colored(f"\tProbably claimed {title}",'green')+'\n\t The above could be a false positive if the list of wanted characters has the name of another user\'s \nharem name in it, or if your claim timer is on cooldown')
            
            except IndexError: #if no reactions
                print(colored(f"\tThere was no reactions on {title}, so reacting with default emoji",'yellow'))

                try: 
                    await message.add_reaction("❤️")
                    print(colored(f"\tProbably claimed {title}",'green')+'\n\tThe above could be a false positive if the list of wanted characters has the name of another user\'s harem name in it, or if your claim timer is on cooldown')

                except Exception as e: #if anything goes wrong claiming by adding our own reaction, print the exception
                    print(colored(f'\tCould not claim {title} because {e}', 'red'))
            except Exception as e: #if anything goes wrong claiming normally
                print(colored(f'\tCould not claim {title} because {e}', 'red'))

        else: #used so the user knows the program is reading the messages successfully.
            print(colored(f"\nIgnoring {title}, in channel '{message.channel}'' because they are not wanted",'yellow'))
    except IndexError: #This IndexError is used to return when there is no Embed
        return

    

    #daily kakera
        
        

    
client.run(TOKEN, bot=False) #if you are reading this, have a nice day OwO, 
                            #and you are probably better  