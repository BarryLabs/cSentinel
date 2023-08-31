## Summary
A discord bot I wrote in python to manage my discord server. It comes with a handful of commands currently available including logging.

## Functions
### Commands
- help - Shows a list of commands.
- about - Shows information about cSentinel.
- ping - Checks the bots latency.
- clear - Clears a specified number of messages.
- role - Displays information about a specified role.
- move - Moves a user to a specified role.
- mute - Moves a user to the muted role. Currently requires a role named "Muted".
- unmute - Moves a user to the unmuted role. Currently requires a role named "Unmuted".
- roll - Rolls a number between 1-100.
- poll - Generates a poll.
- reminder - Sets a text reminder.
- sInvite - Generates a server invite.
- bInvite - Generates a bot invite.
- uInfo - Displayes information about a specified user.
- sInfo - Displays information about the server.

### Events
- The bot will welcome new users.


## Installation
The following will assume you have your discord developer application set up already in which case you can either run the script as a python script or make it executable.

Alternatively, I will put in a more detailed guide here...

To partake, you'll have to create a discord application on their developer portal; [https://discord.com/developers/applications](https://discord.com/developers/applications). Once created, you will have to go to the Bot sidebar so that you can set the privileged gateway intents (all of them 'on'). Then you will need to add the bot to your server in the Bot tab as well as grab the token from the same tab. You will need to hit "Reset Token" in order to get the token. Once completed, you should be good to go to configure the config.py file with the proper TOKEN and then run the cSentinelInitializer.py file and you should be able to see the bot successfully join your server.
