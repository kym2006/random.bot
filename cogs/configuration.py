import discord
from discord.ext import commands
from classes import converters
import json 
import shelve
class Configuration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.command(
        description="Change the prefix or view the current prefix.", usage="prefix [new prefix]", aliases=["setprefix"]
    )
    async def prefix(self, ctx, *, prefix: str = None):
        if prefix is None:
            with shelve.open('prefix') as shelf:
                res = self.bot.config.default_prefix if shelf[str(ctx.guild.id)] is None else shelf[str(ctx.guild.id)]
            await ctx.send(
                embed=discord.Embed(
                    description=f"The prefix for this server is `{res}`.",
                    colour=self.bot.primary_colour,
                )
            )
            return
        if ctx.author.guild_permissions.administrator is False:
            raise commands.MissingPermissions(["administrator"])
        else:
            if len(prefix) > 10:
                await ctx.send(
                    embed=discord.Embed(
                        description="The chosen prefix is too long.",
                        colour=self.bot.error_colour,
                    )
                )
                return
            if prefix == self.bot.config.default_prefix:
                prefix = None
            await self.bot.get_data(ctx.guild.id)
            async with self.bot.pool.acquire() as conn:
                await conn.execute("UPDATE data SET prefix=$1 WHERE guild=$2", prefix, ctx.guild.id)
            with shelve.open('prefix') as shelf:
                shelf[str(ctx.guild.id)] = prefix
            await ctx.send(
                embed=discord.Embed(
                    description="Successfully changed the prefix to "
                    f"`{self.bot.config.default_prefix if prefix is None else prefix}`.",
                    colour=self.bot.primary_colour,
                )
            )

    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    @commands.command(
        name="toggleping",
        usage="toggleping",
        description="toggle between pinging a user or not",
    )
    async def toggleping(self, ctx):
        async with self.bot.pool.acquire() as conn:
            row = await conn.fetchrow("SELECT * FROM data WHERE guild=$1", ctx.guild.id)
        if row is None:
            async with self.bot.pool.acquire() as conn:
                await conn.execute(
                    """INSERT INTO data(guild, ping) VALUES($1, $2)""",
                    ctx.guild.id,
                    False,
                )
        async with self.bot.pool.acquire() as conn:
            row = await conn.fetchrow("SELECT * FROM data WHERE guild=$1", ctx.guild.id)
        async with self.bot.pool.acquire() as conn:
            await conn.execute(
                """
        UPDATE data
        SET ping=$1
        WHERE guild=$2
        """,
                bool(1 - (0, row["ping"])[row["ping"] is not None]),
                ctx.guild.id,
            )
        await ctx.send("Successfuly updated your settings!")


    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    @commands.command(
        description="Set cooldown on commands",
        usage="setcooldown [command name] [time(in seconds)]",
        aliases=["cooldown", "setcd", "cd"]
    )
    async def setcooldown(self, ctx, command:str, ti:int):
        jsb= (await (self.bot.get_data(ctx.guild.id)))['cooldown']
        if jsb is None:
            jsb = "{}"
        dat=json.loads(jsb)
        dat[command] = ti 
        if ctx.guild.id not in self.bot.cooldown:
            self.bot.cooldown[ctx.guild.id] = dict()
        self.bot.cooldown[ctx.guild.id][command] = ti
        async with self.bot.pool.acquire() as conn:
            await conn.execute("UPDATE data set cooldown=$1 where guild=$2", json.dumps(dat), ctx.guild.id)
        await ctx.send("Settings updated!")
    @commands.guild_only()
    @commands.command(description="View the configurations for the current server.", usage="viewconfig")
    async def viewconfig(self, ctx):
        data = await self.bot.get_data(ctx.guild.id)
        byebyeroles=data['byebyeroles']
        if byebyeroles is None:
            byebyeroles=[]
        embed = discord.Embed(title="Server Configurations", colour=self.bot.primary_colour)
        embed.add_field(name="Prefix", value=self.bot.tools.get_prefix(self.bot, ctx.guild),inline=False)
        embed.add_field(name=f"Ping(for {ctx.prefix}someone, {ctx.prefix}wheel etc", value=data['ping'],inline=False)
        embed.add_field(name="Roles with access to iamveryrandom/byebye", value="*Not set*" if len(byebyeroles) == 0 else " ".join([f"<@&{str(i)}>" for i in byebyeroles]),inline=False)
        await ctx.send(embed=embed)

    

def setup(bot):
    bot.add_cog(Configuration(bot))
