"""Cog for displaying the subscriber count of a youtube channel in a channel topic"""

import os
import asyncio

import aiohttp
import discord
from discord.ext import commands


class Subcount:

    def __init__(self, bot):
        self.bot = bot

        self.params = {
            'part': 'statistics',
            'id': self.bot.config.cogs['subscriber_count']['channel_name'],
            'key': self.bot.config.cogs['subscriber_count']['key']
        }

        self.bot.loop.create_task(self.update_channel_topic())

    
    async def fetch(self, url, params=None):
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url, params=params) as r:
                res = await r.json()
        return res


    async def update_channel_topic(self):
        await self.bot.wait_until_ready()
        print('Started task : update_channel_topic')
        while not self.bot.is_closed():
            try:
                resp = await self.fetch('https://www.googleapis.com/youtube/v3/channels', self.params)
                subcount = resp['items'][0]['statistics']['subscriberCount']

                numbers = ['0\u20e3', '1\u20e3', '2\u20e3', '3\u20e3', '4\u20e3', '5\u20e3', '6\u20e3', '7\u20e3', '8\u20e3', '9\u20e3']
                formatted = ''
                for char in subcount:
                    formatted += str(numbers[int(char)])

                for channel_id in self.bot.config.cogs['subscriber_count']['text_channels']:
                    channel = self.bot.get_channel(int(channel_id))
                    await channel.edit(topic='Total subscribers: {}'.format(formatted))
            except Exception as e:
                print('-'*20, 'update_channel_topic encountered error :', e, sep='\n')
            await asyncio.sleep(30)


def setup(bot):
    bot.add_cog(Subcount(bot))