# mudaeautoclaimer-roller
A python program that can allow the user to automatically claim and roll waifus/husbandos with Mudae bot.


# WARNING: 
AUTOMATING USERS IS AGAINST DISCORD'S TOS. IT IS ALSO FORBIDDEN BY MANY SERVERS, SO USE AT YOUR OWN RISK. 
I am 99.99999% sure nothing will happen to your account if you do use this, but still things can happen. I am not responsible for any accounts getting banned. This code was created for purely educational purposes.


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

"timeBetweenRolls": The amount of time between consecutive rolls in a channel for the program. The lower it is set, the more likely Mudae won't register your inputs, and the less human you will seem.

"command": The command that will be used for rolling.

"numberOfRolls": The amount of max rolls the program will show. Basically doesn't affect anything except the what it says in the console

"dkCommand": The command that will be used for daily kakera claiming

"dailyCommand": The command that will be used for getting $daily

"claimByClaimRank": Allows the ability to claim by a character's claim rank. Must be true or false. (Can only be used on servers that have $toggleclaimrolls enabled). If the server has it disabled, then the bot will automatically not use this feature.

"claimRank": The minimum claim rank for the bot to claim solely by claim rank. This does not override claiming by character or claiming by series.

"claimByKakera": Allows the ability to claim by a character's kakera value. Must be true or false. (Can only be used on servers that have $togglekakerarolls enabled). If the server has it disabled, then the bot will automatically not use this feature.

"kakeraValue": The kakera threshold for claiming a character by kakera value. In other words, the minimum amount of kakera a character must be worth for the program to claim solely by kakera value. This does not override claiming by character or claiming by series.


# To add in the future: 

1. Kakera Claiming (I really need to get going on this lmao)
2. A config setup gui
3. Probably stuff

# worst fails so far because I didn't implement checking claim cooldown :( 
![image](https://user-images.githubusercontent.com/79847791/114407634-9862f380-9b76-11eb-90d3-621d4123b34f.png) 
nevermind actually got her 3 days later
