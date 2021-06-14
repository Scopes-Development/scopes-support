import discord
from discord.ext import commands
from discord_slash import SlashCommand
from discord_slash import cog_ext
import json

guild_id = [774402229737488385]


class Rules(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="ping", guild_ids=guild_id, help="Display the bot's latency")
    async def ping(self, ctx, arg):
        embed = discord.Embed(
            colour=ctx.author.color,
            title="🏓Pong!",
            description=f'Latency : **{round(self.bot.latency * 1000)}ms**'
        )
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Rules(bot))
