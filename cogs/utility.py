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

    @cog_ext.cog_slash(name="devs", guild_ids=guild_id, description="View a list of our developers")
    async def devs(self, ctx):
        embed = discord.Embed(color=ctx.author.color)
        role = ctx.guild.get_role(803680355022274640)

        for member in role.members:
            embed.add_field(
                name=member.name, value=f"ID : `{member.id}`\nUser : `{member}`", inline=False)

        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="bots", guild_ids=guild_id, description="View a list of our bots")
    async def bots(self, ctx):
        list = bots_list()

        embed = discord.Embed(
            color=ctx.author.color, description="All the bots made by Scopes Development's <@&803680355022274640>")
        embed.set_author(name="Our Bots", icon_url=ctx.guild.icon_url)

        for bot_id in list:
            bot = get_bot(bot_id)

            embed.add_field(name=f"{self.bot.get_user(bot_id)} [{bot['prefix']}help]",
                            value=f"Made by **{self.bot.get_user(bot['dev'])}** | Created on : `{bot['date']}`\n> **About**\n{bot['about']}", inline=False)

        await ctx.send(embed=embed)

    add_options = [
        {
            "name": "bot_id",
            "description": "ID of the bot",
            "type": 3,
            "required": "true"
        },
        {
            "name": "developer",
            "description": "Mention the bot's developer",
            "type": 6,
            "required": "true"
        },
        {
            "name": "about",
            "description": "Introduction/information about the bot",
            "type": 3,
            "required": "true"
        },
        {
            "name": "creation_date",
            "description": "When was the bot created",
            "type": 3,
            "required": "true"
        },
        {
            "name": "prefix",
            "description": "The bot's default prefix",
            "type": 3,
            "required": "true"
        }
    ]

    @cog_ext.cog_slash(name="addbot", guild_ids=guild_id, description="Add a new bot to Scopes Development's bots", options=add_options)
    @commands.has_role(781239888736944188)
    async def addbot(self, ctx, bots_id, developer: discord.Member, about, date, prefix):
        bot_id = int(bots_id)
        dev_role = ctx.guild.get_role(803680355022274640)
        bot = ctx.guild.get_member(bot_id)

        if dev_role in developer.roles:
            pass
        else:
            developer.add_roles(dev_role)

        for role in bot.roles:
            if role.name == bot.name:
                continue

            if role.name == "@everyone":
                continue

            await bot.remove_roles(role)

        new_roles = [789061944689950722,
                     774406338218164255, 774406153584508988]

        for x in new_roles:
            role = ctx.guild.get_role(x)

            await bot.add_roles(role)

        add_bot(bot.id, about, developer.id, date, prefix)

        embed = discord.Embed(
            color=bot.color, title=f"{bot.name} has been added to Scopes Development's bots!", description=f"Made by **{developer}**\nCreated on : {date}\nAbout : {about}")

        embed.set_author(
            name=f"{bot.name} [{prefix}help]", icon_url=bot.avatar_url)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Rules(bot))
