# Neko-Chan
This is a multi-purpose discord bot written in python 3.5 using discord.py.

## Features
These are some of the features that this bot has got:
 - Access Level System
 - Music bot with queue system
 - Configurable Anti-Spam-System
 - Various moderation tools such as ban, kick, role_add, role_remove e.t.c
 - Deactivatable commands
 - Message logging
 - Anime and Manga information commands
and a lot more.

## What are access levels?
Access levels are a replacement for the roles of a discord server. You are able to assign a access level for a user to give him permissions for certain commands.

## Music bot
The music bot has the following features:
 - Music-Bot owner managemnt
 - Skipping Songs
 - Voting for skips
 - Adding songs to queue
 - Dequeueing songs
 - Changeable volume
 - Changing the volume
 - Auto-Disconnect

### The auto disconnect
The music bot will automatically disconnect from voice channels when the queue runs empty or the bot is left alone in a channel. This way the music bot can change the music channels without having to summon the bot to the user.
This behaviour can be disabled by executing the "autodc" command.

### Music-Bot owner management
Instead of giving each user equal rights to the music bot thus giving trolls a easy platform this bot has an integrated Owner management.
The owner of a music bot is privileged to
 - Skip songs without having to vote
 - Remove songs from the queue.

#### What happens if the Music-Bot owner disconnects?
In case the owner of a music bot disconnects, there are 2 possible reactions.

##### The bot is left alone
If the automatic disconnect feature is enabled, the music bot will automatically disconnect and allow another user to start it again.
If the automatic disconnect feature is disabled the music bot will make the next user that connects to the bots voice channel the new owner

##### There are still users with the music bot
The bot will automatically select a new owner for the music bot.

## Prefixes
This bot does not have a fixed prefix.
The default prefix is "!" tho. If this bot does get in conflict with another bot you may change the syntax my mentioning the bot with the following message:
```config prefix "new_prefix"```


##Configuration:
Please see the file "global_vars.py" for the configuration of the bot
There you'll find all config variables as well as the syntaxes

## I can't host this bot on my own, what now?
If you can't host this bot on your own, you also may use the public hosted bot by using this link:
https://discordapp.com/oauth2/authorize?&client_id=171326146976284672&scope=bot&permissions=535915574

###Hint:
Using the public bot will also enable a couple of new features.
This includes (but is not limited to):
 - A webinterface to change all the bots configurations
 - Fetching RSS feeds to specific channels
 - Additional commands
 - Assigning of discord roles to certain access levels
 - A user database
 - Blacklisting and Whitelisting of users to certain permissions

and more.

Additionally you support the development of this bot. If a error occurs it'll automatically generate a bug report and send it to us. We will take care an fix it as soon as possible.

But the best of all is:

**__It's 100 % free__**

You don't have to worry about server bills. You can focus on using the bot.
