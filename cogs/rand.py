import asyncio
import random
import typing
import discord
from discord.ext import commands
import names 

class Random(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="choose", description="Choose something")
    async def choose(self, ctx, *args):
        await ctx.send("The wheel has chosen {}!".format(random.choice(args)))
    
    @commands.command(name = "colour", aliases = ["color","randomcolour", "randomcolor", "gencolor", "gencolour"], description = "Pick a random colour", usage = "colour")
    async def colour(self, ctx):
        c = discord.Colour.from_rgb(random.randint(0,255), random.randint(0,255), random.randint(0,255))
        await ctx.send(embed=discord.Embed(
            title="Colour codes",
            description=f"6 digit Hexadecimal: ``{c.__str__()}``\n"
                        f"RGB Values: ``{c.to_rgb()}``",
            colour=c
        ))

    @commands.command(name="someone", usage="someone", description="ping someone at random")
    async def mention(self, ctx, allow_bots: str = "0", *, msg: str = ""):
        async with self.bot.pool.acquire() as conn:
            row = await conn.fetchrow("SELECT * FROM data WHERE guild=$1", ctx.guild.id)
        if row and row["ping"] != None and row["ping"] == 1:
            canping = 1
        else:
            canping = 0
        try:
            allow_bots = int(allow_bots)
            if allow_bots:
                user = random.choice(ctx.channel.guild.members)
                if canping:
                    await ctx.send("Picked <@!{}>".format(user.id))
                else:
                    embed = discord.Embed(description="Picked <@!{}>".format(user.id))
                    embed.set_footer(text=f"Use {ctx.prefix}toggleping to toggle between actually pinging the user")
                    await ctx.send(embed=embed)
            else:
                raise KeyboardInterrupt
        except:
            potential = []
            for i in ctx.channel.guild.members:
                if not i.bot:
                    potential.append(i)
            user = random.choice(potential)
            if canping:
                await ctx.send("Picked <@!{}>".format(user.id))
            else:
                embed = discord.Embed(description="Picked <@!{}>".format(user.id))
                embed.set_footer(text=f"Use {ctx.prefix}toggleping to toggle between actually pinging the user")
                await ctx.send(embed=embed)

    @commands.command(name="randint", aliases=["rnd"], description="Pick a number in range <st> to <en>")
    async def rnd(self, ctx, arg1: int, arg2: int):
        await ctx.send("Picked {} from {} to {}".format(random.randrange(arg1, arg2 + 1), arg1, arg2))

    @commands.command(name="username", description="Send the name of someone in the server")
    async def username(self, ctx, allow_bots: str = "0", *, msg: str = ""):
        try:
            allow_bots = int(allow_bots)
            if allow_bots:
                user = random.choice(ctx.channel.guild.members)
                await ctx.send("Picked {}".format(user.name + "#" + str(user.discriminator)))
            else:
                raise KeyboardInterrupt
        except:
            potential = []
            for i in ctx.channel.guild.members:
                if not i.bot:
                    potential.append(i)
            user = random.choice(potential)
            await ctx.send("Picked {}".format(user.name + "#" + str(user.discriminator)))

    @commands.command(name="name", usage="name [gender]", description="Get a english name", aliases=["randomname"])
    async def name(self, ctx, gender:str="Both"):
        gender=gender.lower()
        res=""
        if gender=="male":
            res=names.get_full_name(gender="male")
        elif gender=="female":
            res=names.get_full_name(gender="female")
        else:
            res=names.get_full_name()
        await ctx.send(embed=discord.Embed(
            title="Random Name",
            description=res,
            colour=self.bot.primary_colour
        ))


    @commands.command(name="wheel", description="@someone but more dramatic")
    async def wheel(self, ctx, *, msg: str = ""):
        async with self.bot.pool.acquire() as conn:
            row = await conn.fetchrow("SELECT * FROM data WHERE guild=$1", ctx.guild.id)
        if row and row["ping"] != None and row["ping"] == 1:
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
            msg = await ctx.send(f"\N{ROUND PUSHPIN} {user.name}#{user.discriminator} chosen for the draw.")
            finals.append(user)
            await asyncio.sleep(10)
        user = random.choice(potential)
        if canping:
            await ctx.send(f"Final winner: {random.choice(finals).mention}")
        else:
            embed = discord.Embed(description=f"Final winner: {random.choice(finals).mention}")
            embed.set_footer(text=f"Use {ctx.prefix}toggleping to toggle between actually pinging the user")
            await ctx.send(embed=embed)

    @commands.command(name="card", description = "Draw a random poker card", usage = "card", aliases = ["poker"])
    async def card(self, ctx):
        suit = random.choice(["diamonds", "clubs", "hearts", "spades"])
        num = random.choice(["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"])
        r = random.randint(1,54)
        res = f"{num} of {suit}"
        if r == 1:
            res =  "Red Joker"
        elif r == 2:
            res = "Black Joker"
        await ctx.send(embed=discord.Embed(
            title="Card chosen",
            description=res,
            colour=self.bot.config.primary_colour
        ))

    @commands.command(name="somerole", description="Ping a user with that role in your server")
    async def somerole(self, ctx, role: str):
        async with self.bot.pool.acquire() as conn:
            row = await conn.fetchrow("SELECT * FROM data WHERE guild=$1", ctx.guild.id)
        if row and row["ping"] != None and row["ping"] == 1:
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
        await ctx.send(":8ball: " + random.choice(li))

    @commands.command(name="coinflip", description="Flip a coin. Input a side to bet.")
    async def coinflip(self, ctx, chosen: str = "null"):
        notland = random.randint(1, 6000)  # this chance
        if notland == 1:
            await ctx.send("The coin landed perfectly on it's side! What a miracle!")
            owner = self.bot.get_user(298661966086668290)
            await owner.send(str(ctx.author.id) + " got a perfect coinflip!")
            return
        if chosen == "null":
            sideint = random.randint(1, 2)
            if sideint == 1:
                await ctx.send("The coin landed on tails")
            else:
                await ctx.send("The coin landed on heads")
            return
        if chosen != "heads" and chosen != "tails":
            await ctx.send("Please choose heads or tails only.")
            return
        sideint = random.randint(1, 2)
        side = "heads"

        if sideint == 1:
            side = "tails"
        if side == chosen:
            await ctx.send("The coin landed on {}. You have guessed correct".format(side))
        else:
            await ctx.send("The coin landed on {}. You have guessed wrong".format(side))

    

    @commands.command(name="shuffle", description="Shuffle a list.")
    async def shuffle(self, ctx, *args):
        args = list(args)
        random.shuffle(args)
        res = ""
        for i in args:
            res += i + " "

        await ctx.send(f"Shuffled list: {res}")

    @commands.command(
        name="iamveryrandom",
        usage="iamveryrandom <ban|kick>",
        description="Randomly ban or kick a user, depending on what you input. Person calling this command must have kicking/banning permissions.",
        aliases=["byebye"]
    )
    async def iamveryrandom(self, ctx, kick_or_ban: str = "ban"):
        if kick_or_ban.lower() != "ban" and kick_or_ban.lower() != "kick":
            await ctx.send("Do you want me to ban or kick?")
            return
        member = ctx.guild.get_member(ctx.author.id)
        if kick_or_ban.lower() == "ban" and not member.guild_permissions.ban_members:
            await ctx.send("You do not have permissions in this server to use this command.")
            return
        if kick_or_ban.lower() == "kick" and not member.guild_permissions.kick_members:
            await ctx.send("You do not have permissions in this server to use this command.")
            return
        user = random.choice(ctx.channel.guild.members)
        await ctx.send("Picked <@!{}>".format(user.id))
        await ctx.send("Say your goodbyes...")
        if kick_or_ban.lower() == "ban":

            await ctx.send("Banning in 10 seconds... ")
            await self.bot.change_presence(activity=discord.Game("Banning someone"))
            await asyncio.sleep(10)
            await self.bot.change_presence(
                activity=discord.Game("@help | @someone | being random on {} servers".format(len(self.bot.guilds)))
            )
            try:
                await ctx.channel.guild.ban(
                    user,
                    reason=f"Random ban requested by {ctx.author.name}#{ctx.author.discriminator}",
                    delete_message_days=0,
                )
            except:
                await ctx.send("I need higher perms than that person.")
                return
            await ctx.send("Goodbye!")
            await self.bot.change_presence(
                activity=discord.Game("@help | @someone | being random on {} servers".format(len(self.bot.guilds)))
            )
        else:
            await ctx.send("Kicking in 10 seconds... ")
            await self.bot.change_presence(activity=discord.Game("Kicking someone"))
            await asyncio.sleep(10)
            await self.bot.change_presence(
                activity=discord.Game("@help | @someone | being random on {} servers".format(len(self.bot.guilds)))
            )
            try:
                await ctx.channel.guild.kick(
                    user,
                    reason=f"Random kick requested by {ctx.author.name}#{ctx.author.discriminator}",
                )
            except:
                await ctx.send("I need higher perms than that person.")
                return
            await ctx.send("Goodbye!")
            await self.bot.change_presence(
                activity=discord.Game("@help | @someone | being random on {} servers".format(len(self.bot.guilds)))
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
        n = len(players)
        teams = [[] for i in players]
        for i in range(len(players)):
            teams[i % num].append(players[i])
        embed = discord.Embed(title="Random Teams")
        for i in range(num):
            res = ""
            for j in teams[i]:
                res += f"{j}, "
            res = res[:-2]
            embed.add_field(name=f"Team {i+1}", value=res, inline=False)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Random(bot))
