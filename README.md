# mudaeautoclaimer-roller
A python program that can allow the user to automatically claim and roll waifus/husbandos with Mudae bot.


# WARNING: 
AUTOMATING USERS IS AGAINST DISCORD'S TOS. IT IS ALSO FORBIDDEN BY MANY SERVERS, SO USE AT YOUR OWN RISK. 
I am 99.99999% nothing will happen to your account if you do use this, but still things can happen. I am not responsible for any accounts getting banned. This code was created for purely educational purposes.


# TO USE
1. Paste the channel id of each of the channels that you want the program to run in, separated by new lines, 
into channels.txt

2. Paste the names of each of the characters and or series that you want the program to claim, separated by new lines, into characters/series.txt respectively. The names of each character/series must be the character/series's offical name(the name used for the title of the embed the bot sends), and is **CASE SENSITIVE**.

3. Adjust config.json to your liking (read below)
Also, you need your own user token. I will not give a tutorial here, so just search for how to find it yourself. 

4. Run the program.



# Current config options info:

"reactionDelay": The amount of delay in seconds between the bot seeing something you are interested in and actually reacting to it.  With a higher number, it is more likely that Mudae is able to register the reaction to a character, but the less likely you are to claim first.

"TOKEN": Your user token used to make the program actually work. I can assure you that this program is not a token logger, because I am too stupid to make one of those.
If you feel like your account is in danger, you can download the source code and confirm it is not harmful.

"timeBetweenRolls": The amount of time between consecutive rolls in a channel for the program. The lower it is set, the more likely Mudae won't register your inputs.

"command": The command that will be used for rolling.

"numberOfRolls": The amount of rolls the program will try to do per channel

"typingTime": The amount of time the bot types for before sending a message.



# To add in the future: 

1. Kakera Claiming 
2. Auto $daily
3. A Setup gui
4. Probably stuff



