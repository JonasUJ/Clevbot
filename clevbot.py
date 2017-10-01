"""Bot that interacts with the cleverbot.com api"""

import json

import aiohttp
import discord
from discord.ext import commands

class Empty(object):
    pass

config = Empty()
with open('config.json') as fp:
    c = json.load(fp)
for k, v in c.items():
    setattr(config, k, v)
bot = commands.Bot(command_prefix=None)
bot.convs = dict()


async def respond(msg, query):

    if not query:
        return 'Sorry, but you didn\'t ask anything :/ do `@{} what\'s your name?` to ask me what my name is!'.format(bot.user.display_name)

    if msg.author in bot.convs.keys():
        cs = bot.convs[msg.author]
    else:
        cs = ""

    params = {
        "key": config.Cleverbot_api_key,
        "cs": cs,
        "input": query
    }

    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.cleverbot.com/getreply', params=params) as r:
            res = await r.json()
            bot.convs[msg.author] = res['cs']
            return res['output']

@bot.event
async def on_message(msg):
    if msg.content.startswith(bot.user.mention):
        async with msg.channel.typing():
            await msg.channel.send('{} {}'.format(msg.author.mention, await respond(msg, msg.content.strip(bot.user.mention))))

@bot.event
async def on_ready():
    print('Logged in as:', bot.user.name)
    print('Id:', bot.user.id)
    await bot.change_presence(game=discord.Game(name='@{} to chat with me'.format(bot.user.display_name), type=0))

if __name__ == '__main__':
    bot.run(config.Bot_token)