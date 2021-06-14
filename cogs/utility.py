import discord
from discord.ext import commands
from discord_slash import SlashCommand
from discord_slash import cog_ext
from main import *
from discord.ext.commands import cooldown, BucketType
from discord.ext.commands import CommandOnCooldown

guild_id = [774402229737488385]


class Rules(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="ping", guild_ids=guild_id, description="Display the bot's latency")
    async def ping(self, ctx, arg):
        embed = discord.Embed(
            colour=ctx.author.color,
            title="🏓Pong!",
            description=f'Latency : **{round(self.bot.latency * 1000)}ms**'
        )
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="host", guild_ids=guild_id, description="Know what hosting service we use!")
    async def host(self, ctx):
        embed = discord.Embed(color=discord.Color.purple(), title="Sweplox Hosting", url="https://sweplox.net",
                              description="We use [sweplox.net](https://sweplox.net 'Sweplox Hosting panel') to host all our bots on the lowest ping possible and the best processors!")

        embed.add_field(
            name="🔗Links", value="[Discord Server](https://discord.gg/XPvZqsHu 'Sweplox Hosting discord server')\n[Game Panel](https://game.panel.sweplox.net 'Game panel/Control panel of your servers on Sweplox Hosting')\n[ARC.io AFK page](https://client.sweplox.net/arcio 'Earn coins and upgrade your resources with them by being AFK on this page.')\n[Client Page](https://client.sweplox.net 'Sweplox Hosting client page')")

        embed.set_thumbnail(
            url="https://cdn.discordapp.com/icons/582928406794993664/a_61b8630f5f0759d8d24c74259940c9e5.gif?size=4096")
        await ctx.send(embed=embed)

    submit_options = [
        {
            "name": "name",
            "description": "Name of the bot",
            "type": 3,
            "required": "true"
        },
        {
            "name": "description",
            "description": "Describe your idea as much as possible so we can give the closest result to your vision",
            "type": 3,
            "required": "true"
        }
    ]

    @cog_ext.cog_slash(name="submit", guild_ids=guild_id, description="Submit your bot idea and we will make it happen!", options=submit_options)
    async def submit(self, ctx, name, description):
        code = add_idea(ctx.author.id, name, description)
        embed = discord.Embed(
            color=ctx.author.color, title=f"Idea #{code}", description=f"Submitted by : {ctx.author} ({ctx.author.id})")
        embed.add_field(name=name, value=description)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        ch = self.bot.get_channel(854136124423405608)
        await ch.send(embed=embed)

        await ctx.send(f"Your bot idea has been submitted to us! The idea's ID : {code}", delete_after=5)


def setup(bot):
    bot.add_cog(Rules(bot))
