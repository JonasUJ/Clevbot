"""Bot that interacts with the cleverbot.com api"""

import os
import json
from urllib.parse import quote

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
bot.config = config


async def respond(msg, query):
    print('-'*20)

    if not query:
        return 'Sorry, but you didn\'t ask anything :/ do `@{} what\'s your name?` to ask me what my name is!'.format(bot.user.display_name)
    print('Input query from {} : {}'.format(msg.author, query))

    if msg.author in bot.convs.keys():
        cs = bot.convs[msg.author]
    else:
        cs = ""

    params = {
        "key": config.Cleverbot_api_key,
        "cs": cs,
        "input": quote(query)
    }

    print('Sending "{}" to cleverbot'.format(params['input']))
    try:
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://www.cleverbot.com/getreply', params=params) as r:
                res = await r.json(encoding='utf-8')
                bot.convs[msg.author] = res['cs']
                print('Response from cleverbot : {}'.format(res['output']))
                return res['output']
    except Exception as e:
        print('Something went wrong contacting cleverbot : {}'.format(e))

@bot.event
async def on_message(msg):
    if msg.content.startswith(bot.user.mention):
        async with msg.channel.typing():
            await msg.channel.send('{} {}'.format(msg.author.mention, await respond(msg, msg.content.strip(bot.user.mention).strip(' '))))

@bot.event
async def on_ready():
    print('-'*20)
    print('Logged in as:', bot.user.name)
    print('Id:', bot.user.id)
    await bot.change_presence(game=discord.Game(name='@{} to chat with me'.format(bot.user.display_name), type=0))

if __name__ == '__main__':

    # Load extensions
    for cog in os.listdir('cogs'):
        name, extension = os.path.splitext(cog)
        if extension == '.py':
            bot.load_extension('cogs.{}'.format(name))
            print('Loaded cog :', name)

    bot.run(config.Bot_token)