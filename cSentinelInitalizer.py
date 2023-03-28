import config
import asyncio
import discord
from discord.ext import commands
import random
import logging
import logging.handlers
import requests
import json

# Intents
bot = commands.Bot(command_prefix=config.PREFIX, intents=discord.Intents.all())

# Initializer
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(f"{config.PREFIX}help"))
    print(f"Bot Initialized.")

# Commands

@bot.remove_command('help')

@bot.command(name='help', description='Shows a list of available commands.')
async def help(ctx):
    embed = discord.Embed(title="Help Menu", colour=discord.Colour.green())
    embed.add_field(name='!about', value='Displays information about Sentinel.', inline=False)
    embed.add_field(name='!ping', value='Checks the bot\'s latency.', inline=False)
    embed.add_field(name='!clear', value='Clears a specified number of messages from a text channel.', inline=False)
    embed.add_field(name='!role', value='Displays information about a specified role.', inline=False)
    embed.add_field(name='!move', value='Moves a user to a specified role.', inline=False)
    embed.add_field(name='!mute', value='Moves a user to a muted role. Requires a role named "Muted".', inline=False)
    embed.add_field(name='!unmute', value='Moves a user to the unmuted role. Requires a role named "Unmuted".', inline=False)
    embed.add_field(name='!roll', value='Rolls a number between 1 and 100.', inline=False)
    embed.add_field(name='!poll', value='Generates a poll.', inline=False)
    embed.add_field(name='!reminder', value='Sets a text reminder.', inline=False)
    embed.add_field(name='!sInvite', value='Generates a link to this server.', inline=False)
    embed.add_field(name='!bInvite', value='Generates a link to me.', inline=False)
    embed.add_field(name='!uInfo', value='Displays information about the specified user.', inline=False)
    embed.add_field(name='!sInfo', value='Displays information about the server.', inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def about(ctx):
    await ctx.send(f"I am Sentinel. I am a multi-purpose toolbot created by Mamot to provide information, analytics, music, webhooks and automation.")

@bot.command()
async def ping(ctx):
    await ctx.send(f"{round(bot.latency * 1000, 1)}ms")

@bot.command()
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount)

@bot.command()
async def role(ctx, *, role: discord.Role):
    embed = discord.Embed(title=f'{role.name}', colour=role.colour)
    embed.add_field(name='ID', value=role.id)
    embed.add_field(name='Mentionable', value=role.mentionable)
    embed.add_field(name='Hoisted', value=role.hoist)
    embed.add_field(name='Position', value=role.position)
    embed.add_field(name='Managed', value=role.managed)
    embed.add_field(name='Colour', value=role.colour)
    await ctx.send(embed=embed)

@bot.command()
async def move(ctx, member: discord.Member, *, role: discord.Role):
    await member.add_roles(role)
    await ctx.send(f'{member.mention} has been moved to {role.mention}')

@bot.command()
async def mute(ctx, user: discord.Member): 
    if ctx.author.guild_permissions.manage_roles or ctx.author == ctx.guild.owner:
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        await user.add_roles(role)
        await ctx.send(f"{user} has been muted.")
    else:
        await ctx.send("You do not have permissions to mute/unmute.")

@bot.command()
async def unmute(ctx, user: discord.Member):
    if ctx.author.guild_permissions.manage_roles or ctx.authot == ctx.guild.owner:
        role = discord.utils.get(ctx.guild.roles, name="Unmuted")
        await user.add_roles(role)
        await ctx.sned(f"{user} has been unmuted.")
    else:
        await ctx.send("You do not have permissions to mute/unmute.")

@bot.command()
async def roll(ctx):
    rNumber = random.randint(1, 100)
    await ctx.send(f'{rNumber}')

@bot.command()
async def poll(ctx, question: str, *options: str):
    if len(options) <= 1:
        await ctx.send('You will need more than one option to make a poll.')
        return
    if len(options) > 10:
        await ctx.send('You cannot make a poll for more than 10 different options.') 
    description = []
    for x, option in enumerate(options):
        description += '\n {} {}'.format(x+1, option)
    embed = discord.Embed(title=question, description=''.join(description))
    react_message = await ctx.send(embed=embed)
    for emoji in range (len(options)):
        await react_message.add_reaction('{}⃣'.format(emoji+1))
    embed.set_footer(text='Poll ID: {}'.format(react_message.id))
    await react_message.edit(embed=embed)

@bot.command()
async def reminder(ctx, time: int, *, message):
    await ctx.send(f'Reminder set for {time} minutes.')
    await asyncio.sleep(time * 60)
    await ctx.send(f'{message}')

@bot.command()
async def sInvite(ctx):
    iLink = await ctx.channel.create_invite(max_uses=1)
    await ctx.send(f"Here is a link to join the server: {iLink}")

@bot.command()
async def bInvite(ctx):
    bLink = discord.utils.oauth_url(bot.user.id)
    await ctx.send(f"Here is a link to invite me to your server: {bLink}")

@bot.command()
async def uInfo(ctx, *, member: discord.Member = None):
    member = ctx.author if not member else member
    embed = discord.Embed(title=f"{member}'s info", color=member.color, timestamp=ctx.message.created_at)
    embed.set_thumbnail(url=member.avatar)
    embed.add_field(name="ID:", value=member.id)
    embed.add_field(name="Nickname:", value=member.display_name)
    embed.add_field(name="Created at:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
    embed.add_field(name="Joined at:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
    embed.add_field(name="Bot?", value=member.bot)
    await ctx.send(embed=embed)

@bot.command()
async def sInfo(ctx):
    server = ctx.message.guild
    embed = discord.Embed(title="Server Information", color=0x00ff00)
    embed.add_field(name="Name", value=server.name, inline=True)
    embed.add_field(name="ID", value=server.id, inline=True)
    embed.add_field(name="Owner", value=server.owner, inline=True)
    embed.add_field(name="Members", value=server.member_count, inline=True)
    embed.add_field(name="Created At", value=server.created_at.strftime("%d %b %Y %H:%M"), inline=True)
    await ctx.send(embed=embed)

# Events
@bot.event
async def on_member_join(member):
    channel = member.guild.system_channel
    if channel is not None:
        await channel.send('Welcome {0.mention}!'.format(member))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if 'bleep' in message.content.lower():
        response = requests.get('https://www.bleepingcomputer.com/news/')
        data = response.json()
        data = json.loads(data)
        for article in data['articles']:
            embed = discord.Embed(title=article['title'], description=article['excerpt'], url=article['url'])
            await message.channel.send(embed=embed)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(f"{config.PREFIX}help"))
    print("Bot initialized.")
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
logging.getLogger('discord.http').setLevel(logging.INFO)

handler = logging.handlers.RotatingFileHandler(
    filename='discord.log',
    encoding='utf-8',
    maxBytes=32 * 1024 * 1024,
    backupCount=5,
)

dt_fmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Initialize
bot.run(config.TOKEN, log_handler=None)
