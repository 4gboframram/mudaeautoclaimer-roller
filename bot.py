import discord
import asyncio
import json
import re
config_file=open("config.json",'r')
config=json.load(config_file)

TOKEN = config["TOKEN"]

Channels=open('Channels.txt','r').read().splitlines()
characters=open('characters.txt','r').read().splitlines()
client=discord.Client()
reactionDelay=config["reactionDelay"]
command=config["command"]
timeBetweenRolls=config["timeBetweenRolls"]
numberOfRolls=config["numberOfRolls"]
added_tasks=[]
from colorama import init
from termcolor import colored
init()
class h(Exception):
    pass
def search(string):
    
    temp = re.findall(r'\d+', string)
    res = list(map(int, temp))[1] #gives the number of minutes left.
    return res





async def doRolls():
    for channel in Channels:

        chanel=client.get_channel(int(channel)) 
        await chanel.send(command)
        print(colored(f"Excecuting task: Rolling in channel '{chanel.name}'","cyan"))
        try:

            for i in range(int(numberOfRolls)+2):

                    print(colored(f"\tDoing roll {i+1} in channel: '{chanel.name}' ",'blue'))
                    async for message in client.get_channel(int(channel)).history(limit=2):
                        if 'the roulette is limited to' in message.content and client.user.name in message.content:
                            print(colored(f'\tRolls limited in {chanel.name}, moving on to next task','blue'))
                            raise h
                    await chanel.send(command)
                    await asyncio.sleep(timeBetweenRolls)
        except h:
            continue
            
                    
            


@client.event
async def on_ready():
    print(colored(f'Logged in as {client.user.name}','green'))
    await doRolls()
    a=True
    while a==True:
        print(colored('No more tasks: Sleeping for an hour then rolling again', 'cyan'))
        await asyncio.sleep(3600)
        await doRolls()



@client.event
async def on_message(message):
    if str(message.channel.id) not in Channels:
        return
    
    #autoclaimer
    try:
        if message.embeds[0].author.name in characters: 
            #mudae is weird and uses the author field for the title of its embeds
            try:
                print(colored(f"\n Trying to claim: {str(message.embeds[0].author.name)}",'blue'))
                await asyncio.sleep(reactionDelay)
                await message.add_reaction(message.reactions[0])
                print(colored(f'\tReacted to {message.embeds[0].author.name} with ','blue')+colored(message.reactions[0],'cyan'))
                print(colored(f"\tProbably claimed {message.embeds[0].author.name}",'green')+'\n\t The above could be a false positive if the list of wanted characters has the name of another user\'s harem name in it, or if your claim timer is on cooldown')
            
            except IndexError: #if no reactions
                print(colored(f"\tThere was no reactions on {message.embeds[0].author.name}, so reacting with default emoji",'yellow'))

                try: 
                    await message.add_reaction("❤️")
                    print(colored(f"\tProbably claimed {message.embeds[0].author.name}",'green')+'\n\tThe above could be a false positive if the list of wanted characters has the name of another user\'s harem name in it, or if your claim timer is on cooldown')

                except Exception as e:
                    print(colored(f'\tCould not claim {message.embeds[0].author.name} because {e}', 'red'))
            except Exception as e:
                print(colored(f'\tCould not claim {message.embeds[0].author.name} because {e}', 'red'))
        else:
            print(colored(f"\nIgnoring {message.embeds[0].author.name}, in channel {message.channel} because they are not wanted",'yellow'))
    except IndexError:
        return
        
        

    
client.run(TOKEN, bot=False)