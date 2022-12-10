import discord
from discord.ext import commands
from classes import converters
from discord import app_commands

import json 
import shelve
class Configuration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    '''
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    @app_commands.command(
        name="toggleping",
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
        await ctx.response.send_message("Successfuly updated your settings!")
    
    @commands.guild_only()
    @app_commands.command(description="View the configurations for the current server.")
    async def viewconfig(self, ctx):
        data = await self.bot.get_data(ctx.guild.id)
        byebyeroles=data['byebyeroles']
        if byebyeroles is None:
            byebyeroles=[]
        embed = discord.Embed(title="Server Configurations", colour=self.bot.primary_colour)
        embed.add_field(name="Prefix", value=self.bot.tools.get_prefix(self.bot, ctx.guild),inline=False)
        embed.add_field(name=f"Ping(for /someone, /wheel etc", value=data['ping'],inline=False)
        embed.add_field(name="Roles with access to iamveryrandom/byebye", value="*Not set*" if len(byebyeroles) == 0 else " ".join([f"<@&{str(i)}>" for i in byebyeroles]),inline=False)
        await ctx.response.send_message(embed=embed)
    # TODO: configure iamveryrandom roles
    '''
async def setup(bot):
    await bot.add_cog(Configuration(bot))
