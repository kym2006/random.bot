import asyncio
import json
import random
import typing

import aiohttp
import discord
import namegenerator
import names
from discord.ext import commands


class Random(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="choose", description="Choose something", usage="choose <item1 item2 item3...>")
    async def choose(self, ctx, *args):
        await ctx.send(embed=discord.Embed(description="The wheel has chosen {}!".format(random.choice(args)), colour=self.bot.primary_colour))

    @commands.command(
        name="colour",
        aliases=["color", "randomcolour", "randomcolor", "gencolor", "gencolour"],
        description="Pick a random colour",
        usage="colour",
    )
    async def colour(self, ctx):
        c = discord.Colour.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        await ctx.send(
            embed=discord.Embed(
                title="Colour Codes",
                description=f"6 digit Hexadecimal: ``{c.__str__()}``\n" f"RGB Values: ``{c.to_rgb()}``",
                colour=c,
            )
        )
    @commands.command(name = "avatar", description="Get a random avatar! Note: May be subjected to copyright, please contact owner of that avatar before using it.", usage= "avatar")
    async def avatar(self, ctx):
        user = random.choice(self.bot.users)
        default_avatars=[]
        for i in range(5):
            default_avatars.append(f"https://cdn.discordapp.com/embed/avatars/{i}.png")
        while str(user.avatar_url) in default_avatars:
            user=random.choice(self.bot.users)
        embed=discord.Embed(colour=self.bot.config.primary_colour,description="Here's a random avatar! Please do not use it without permission from the original creator.")
        embed.set_thumbnail(url=user.avatar_url)
        embed.set_author(name=f"{user.name}#{user.discriminator}")
        await ctx.send(embed=embed)


    @commands.command(name="someone", usage="someone", description="ping someone at random")
    async def mention(self, ctx, *, msg: str = ""):
        async with self.bot.pool.acquire() as conn:
            row = await conn.fetchrow("SELECT * FROM data WHERE guild=$1", ctx.guild.id)
        if row and row["ping"] is not None and row["ping"] == 1:
            canping = 1
        else:
            canping = 0
        potential = []
        for i in ctx.channel.guild.members:
            if not i.bot:
                potential.append(i)
        user = random.choice(potential)
        if canping:
            await ctx.send("Picked <@!{}>".format(user.id))
        else:
            embed = discord.Embed(description="Picked <@!{}>".format(user.id), colour=self.bot.primary_colour)
            embed.set_footer(text=f"Use {ctx.prefix}toggleping to toggle between actually pinging the user")
            await ctx.send(embed=embed)

    @commands.command(
        name="randint",
        aliases=["rnd"],
        description="Pick a number in range <st> to <en>",
        usage="randint <start> <end>",
    )
    async def rnd(self, ctx, arg1: int, arg2: int):
        await ctx.send(
            embed=discord.Embed(
                description="Picked {} from {} to {}".format(random.randrange(arg1, arg2 + 1), arg1, arg2),
                colour=self.bot.primary_colour,
            )
        )

    @commands.command(name="username", description="Send the name of someone in the server")
    async def username(self, ctx, allow_bots: str = "0", *, msg: str = ""):
        potential = []
        for i in ctx.channel.guild.members:
            if not i.bot:
                potential.append(i)
        user = random.choice(potential)
        await ctx.send(
            embed=discord.Embed(
                description="Picked {}".format(user.name + "#" + str(user.discriminator)),
                colour=self.bot.primary_colour,
            )
        )

    @commands.command(name="name", usage="name [gender]", description="Get a english name", aliases=["randomname"])
    async def name(self, ctx, gender: str = "Both"):
        gender = gender.lower()
        res = ""
        if gender == "male":
            res = names.get_full_name(gender="male")
        elif gender == "female":
            res = names.get_full_name(gender="female")
        else:
            res = names.get_full_name()
        await ctx.send(embed=discord.Embed(title="Random Name", description=res, colour=self.bot.primary_colour))

    @commands.command(name="ign", usage="ign", description="Get an in game name", aliases=["gamename"])
    async def ign(self, ctx):
        res = namegenerator.gen()
        await ctx.send(embed=discord.Embed(title="Random Game Name", description=res, colour=self.bot.primary_colour))

    @commands.command(name="wheel", description="@someone but more dramatic")
    async def wheel(self, ctx, *, msg: str = ""):
        async with self.bot.pool.acquire() as conn:
            row = await conn.fetchrow("SELECT * FROM data WHERE guild=$1", ctx.guild.id)
        if row and row["ping"] is not None and row["ping"] == 1:
            canping = 1
        else:
            canping = 0
        potential = []
        for i in ctx.channel.guild.members:
            if not i.bot:
                potential.append(i)
        finals = []
        for i in range(random.randint(2, 8)):
            user = random.choice(potential)
            await ctx.send(f"\N{ROUND PUSHPIN} {user.name}#{user.discriminator} chosen for the draw.")
            finals.append(user)
            await asyncio.sleep(10)
        user = random.choice(potential)
        if canping:
            await ctx.send(f"Final winner: {random.choice(finals).mention}")
        else:
            embed = discord.Embed(
                description=f"Final winner: {random.choice(finals).mention}", colour=self.bot.primary_colour
            )
            embed.set_footer(text=f"Use {ctx.prefix}toggleping to toggle between actually pinging the user")
            await ctx.send(embed=embed)

    @commands.command(name="card", description="Draw a random poker card", usage="card", aliases=["poker"])
    async def card(self, ctx):
        cards = self.bot.get_guild(623564336052568065).emojis
        suit = random.choice(["eclubs", "espades", "ehearts", "ediamonds"])
        num = random.choice(["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"])
        if suit in ["eclubs", "espades"]:
            num = "b" + num
        else:
            num = "r" + num
        p1, p2 = None, None
        for i in cards:
            if i.name == num:
                p1 = i
        for i in cards:
            if i.name == suit:
                p2 = i
        p1 = str(p1)
        p2 = str(p2)
        await ctx.send(
            embed=discord.Embed(title="Card chosen", description=p1 + "\n" + p2, colour=self.bot.config.primary_colour)
        )

    @commands.command(name="somerole", description="Ping a user with that role in your server")
    async def somerole(self, ctx, role: str):
        async with self.bot.pool.acquire() as conn:
            row = await conn.fetchrow("SELECT * FROM data WHERE guild=$1", ctx.guild.id)
        if row and row["ping"] is not None and row["ping"] == 1:
            canping = 1
        else:
            canping = 0
        users = []
        role = role.replace("<", "")
        role = role.replace(">", "")
        role = role.replace("@", "")
        role = role.replace("&", "")
        role = discord.utils.get(ctx.message.guild.roles, id=int(role))
        for member in ctx.message.guild.members:
            if role in member.roles:
                users.append(member)
        user = random.choice(users)
        if canping:
            await ctx.send("Picked {}".format(user.mention))
        else:
            embed = discord.Embed(description="Picked {}".format(user.mention))
            embed.set_footer(text=f"Use {ctx.prefix}toggleping to toggle between actually pinging the user")
            await ctx.send(embed=embed)

    @commands.command(name="8ball", description="classic 8ball", aliases=["eightball"])
    async def eightball(self, ctx, question: str):
        li = [
            "It is certain.",
            "It is decidedly so.",
            "Without a doubt.",
            "Yes - definitely.",
            "You may rely on it.",
            "As I see it, yes.",
            "Most likely.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Very doubtful.",
        ]
        await ctx.send(embed=discord.Embed(description=":8ball: " + random.choice(li), colour=self.bot.primary_colour))

    @commands.command(name="coinflip", description="Flip a coin", usage="coinflip")
    async def coinflip(self, ctx):
        notland = random.randint(1, 6000)
        if notland == 1:
            await ctx.send(
                embed=discord.Embed(
                    description="The coin landed perfectly on it's side! What a miracle!",
                    colour=self.bot.primary_colour,
                )
            )

        guild = self.bot.get_guild(725303414220914758)
        heads = [e for e in guild.emojis if e.name == "washingtonheads"][0]
        tails = [e for e in guild.emojis if e.name == "washingtontails"][0]
        await ctx.send(str(random.choice([heads, tails])))

    @commands.command(name="dice", description="Throw a 6 side dice!", usage="dice")
    async def dice(self, ctx):
        res = random.randint(1, 6)
        guild = self.bot.get_guild(725303414220914758)
        emoji = [e for e in guild.emojis if e.name == f"dice{res}"][0]
        await ctx.send(emoji)

    @commands.command(name="shuffle", description="Shuffle a list.")
    async def shuffle(self, ctx, *args):
        args = list(args)
        random.shuffle(args)
        res = ""
        for i in args:
            res += i + " "
        await ctx.send(embed=discord.Embed(title="Shuffled List", description=f"{res}", colour=self.bot.primary_colour))

    @commands.command(
        name="iamveryrandom",
        usage="iamveryrandom <ban|kick>",
        description="Randomly ban or kick a user, depending on what you input. Person calling this command must have kicking/banning permissions.",
        aliases=["byebye"],
    )
    async def iamveryrandom(self, ctx, kick_or_ban: str = "ban"):
        if kick_or_ban.lower() != "ban" and kick_or_ban.lower() != "kick":
            await ctx.send("Do you want me to ban or kick?")
            return
        member = ctx.guild.get_member(ctx.author.id)
        if kick_or_ban.lower() == "ban" and not member.guild_permissions.ban_members:
            raise commands.MissingPermissions(["ban_members"])
        if kick_or_ban.lower() == "kick" and not member.guild_permissions.kick_members:
            raise commands.MissingPermissions(["kick_members"])
        user = random.choice(ctx.channel.guild.members)
        await ctx.send("Picked <@!{}>".format(user.id))
        await ctx.send("Say your goodbyes...")
        if kick_or_ban.lower() == "ban":

            await ctx.send("Banning in 10 seconds... ")
            await self.bot.change_presence(activity=discord.Game("Banning someone"))
            await asyncio.sleep(10)
            await self.bot.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.watching, name=f"?help | random on {len(self.bot.guilds)} servers"
                )
            )
            try:
                await ctx.channel.guild.ban(
                    user,
                    reason=f"Random ban requested by {ctx.author.name}#{ctx.author.discriminator}",
                    delete_message_days=0,
                )
            except Exception:
                await ctx.send("I need higher perms than that person.")
                return
            await ctx.send("Goodbye!")
            await self.bot.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.watching, name=f"?help | random on {len(self.bot.guilds)} servers"
                )
            )
        else:
            await ctx.send("Kicking in 10 seconds... ")
            await self.bot.change_presence(activity=discord.Game("Kicking someone"))
            await asyncio.sleep(10)
            await self.bot.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.watching, name=f"?help | random on {len(self.bot.guilds)} servers"
                )
            )
            try:
                await ctx.channel.guild.kick(
                    user,
                    reason=f"Random kick requested by {ctx.author.name}#{ctx.author.discriminator}",
                )
            except Exception:
                await ctx.send("I need higher perms than that person.")
                return
            await ctx.send("Goodbye!")
            await self.bot.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.watching, name=f"?help | random on {len(self.bot.guilds)} servers"
                )
            )

    @commands.command(
        name="team",
        description="Assign random teams players",
        usage="team {number of teams} [players]",
    )
    async def teams(self, ctx, num: typing.Optional[int] = 2, *players):
        num = min(num, len(players))
        players = list(players)
        random.shuffle(players)
        teams = [[] for i in players]
        for i in range(len(players)):
            teams[i % num].append(players[i])
        embed = discord.Embed(title="Random Teams", colour=self.bot.primary_colour)
        for i in range(num):
            res = ""
            for j in teams[i]:
                res += f"{j}, "
            res = res[:-2]
            embed.add_field(name=f"Team {i+1}", value=res, inline=False)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Random(bot))
