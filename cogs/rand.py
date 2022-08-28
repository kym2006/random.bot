import asyncio
import json
import random
import typing
import spintax
import aiohttp
import discord
import namegenerator
import time 
import names
from discord.ext import commands
from classes import converters
from discord import app_commands
cooldown = dict({"randint":dict()})
def get_cd(bot, guild, cmd):
    try:
        cd = bot.cooldown[guild][cmd]
        return 0 if cd is None else cd
    except KeyError:
        return 0
class Random(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    def on_cooldown(self, cmd, id, guild):
        return False

    @app_commands.command(name="reactions", description="Choose some users from those who reacted to a message")
    async def reactions(self, ctx, message_id: str, num: int = 1):
        await ctx.guild.chunk()
        async with self.bot.pool.acquire() as conn:
            row = await conn.fetchrow("SELECT * FROM data WHERE guild=$1", ctx.guild.id)
        if row and row["ping"] is not None and row["ping"] == 1:
            canping = 1
        else:
            canping = 0

        chnl = ctx.channel
        msg = await chnl.fetch_message(int(message_id))
        users = set()
        for reaction in msg.reactions:
            async for user in reaction.users():
                users.add(user)
        res=""
        while num > 0:
            num -= 1
            user = random.choice(list(users))
            users.remove(user)
            res += ("Picked <@!{}> ({}#{})".format(user.id, user.name, user.discriminator))

        if canping:
            await ctx.response.send_message(res)
        else:
            await ctx.response.send_message(embed=discord.Embed(description=res, colour=self.bot.primary_colour))


    @app_commands.command(name="yesno", description="Say yes or no. ")
    async def yesno(self, ctx):
        c = random.choice(["Yes", "No"])
        await ctx.response.send_message(c)
    
    @app_commands.command(name="choose", description="Choose something. Separate choices with comma")
    async def choose(self, ctx, *, choices:str):
        choices = choices.split(",")
        await ctx.response.send_message(embed=discord.Embed(description="The wheel has chosen **{}**!".format(random.choice(choices)), colour=self.bot.primary_colour))
    

    @app_commands.command(name="emoji", description="Send a random emoji")
    async def emoji(self,ctx):
        emojis=[]
        for i in self.bot.guilds:
            emojis.extend(i.emojis)
        await ctx.response.send_message(random.choice(emojis))

    @app_commands.command(name="someonevc", description="Choose someone in your vc.")
    async def someonevc(self, ctx):
        await ctx.guild.chunk()
        voice_state = ctx.user.voice
        if voice_state is None:
            await ctx.response.send_message("You need to be in a voice channel to use this command.")
            return
        await ctx.response.send_message(random.choice(voice_state.channel.members))
        '''
        for i in ctx.guild.channels:
            if type(i) == type(self.bot.get_channel(725303414363390018)):
                member_ids = list(i.voice_states.keys())
                if ctx.author.id in member_ids:
                    chosen = random.choice(member_ids)
                    li = await ctx.guild.query_members(user_ids=[chosen])
                    await ctx.response.send_message(f"{str(li[0])} has been chosen!")
        '''
    '''
    @app_commands.command(name="chose", description="Choose, but rigged to always pick the second item")
    async def chose(self, ctx, *args):
        if len(args) == 1:
            await ctx.response.send_message(embed=discord.Embed(description="The wheel has chosen **{}**!".format(args[0]), colour=self.bot.primary_colour))
        else:
            await ctx.response.send_message(embed=discord.Embed(description="The wheel has chosen **{}**!".format(args[1]), colour=self.bot.primary_colour))
    '''
    @app_commands.command(
        name="colour",
        description="Pick a random colour",
    )
    async def colour(self, ctx):
        c = discord.Colour.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        await ctx.response.send_message(
            embed=discord.Embed(
                title="Colour Codes",
                description=f"6 digit Hexadecimal: ``{c.__str__()}``\n" f"RGB Values: ``{c.to_rgb()}``",
                colour=c,
            )
        )

    @app_commands.command(name = "avatar", description="Get a random avatar!")
    async def avatar(self, ctx):
        await ctx.guild.chunk()
        user = random.choice(self.bot.users)
        default_avatars=[]
        for i in range(5):
            default_avatars.append(f"https://cdn.discordapp.com/embed/avatars/{i}.png")
        while str(user.avatar) in default_avatars:
            user = random.choice(self.bot.users)
        embed=discord.Embed(colour=self.bot.config.primary_colour, description="Here's a random avatar! Please do not use it without permission from the original creator.")
        embed.set_thumbnail(url=user.avatar)
        embed.set_author(name=f"{user.name}#{user.discriminator}")
        await ctx.response.send_message(embed=embed)

    @app_commands.command(name="someone", description="ping someone at random")
    async def mention(self, ctx, *, num: int = 1):
        await ctx.guild.chunk()
        async with self.bot.pool.acquire() as conn:
            row = await conn.fetchrow("SELECT * FROM data WHERE guild=$1", ctx.guild.id)
        if row and row["ping"] is not None and row["ping"] == 1:
            canping = 1
        else:
            canping = 0
        potential = []
        async for i in ctx.guild.fetch_members(limit=None):
            if not i.bot:
                potential.append(i)

        print(potential)
        res = ""
        while num > 0:
            num -= 1
            user = random.choice(potential)
            potential.remove(user)
            res += ("Picked <@!{}> ({}#{})".format(user.id, user.name, user.discriminator))

        if canping:
            await ctx.response.send_message(res)
        else:
            embed = discord.Embed(description=res, colour=self.bot.primary_colour)
            await ctx.response.send_message(embed=embed)

    @app_commands.command(
        name="randint",
        description="Pick a number in range <st> to <en>",
    )
    async def rnd(self, ctx, arg1: int, arg2: int):
        if ctx.guild is None:
            await ctx.response.send_message(
                embed=discord.Embed(
                    description="Picked {} from {} to {}".format(random.randrange(arg1, arg2 + 1), arg1, arg2),
                    colour=self.bot.primary_colour,
                )
            )
            return

        await ctx.response.send_message(
            embed=discord.Embed(
                description="Picked {} from {} to {}".format(random.randrange(arg1, arg2 + 1), arg1, arg2),
                colour=self.bot.primary_colour,
            )
        )

    @app_commands.command(name="username", description="Send the name of someone in the server")
    async def username(self, ctx, allow_bots: str = "0", *, msg: str = ""):
        await ctx.guild.chunk()
        potential = []
        async for i in ctx.guild.fetch_members(limit=None):
            if not i.bot:
                potential.append(i)
        user = random.choice(potential)
        await ctx.response.send_message(
            embed=discord.Embed(
                description="Picked {}".format(user.name + "#" + str(user.discriminator)),
                colour=self.bot.primary_colour,
            )
        )

    @app_commands.command(name="name", description="Get a english name")
    async def name(self, ctx, gender: str = "Both"):
        gender = gender.lower()
        res = ""
        if gender == "male":
            res = names.get_full_name(gender="male")
        elif gender == "female":
            res = names.get_full_name(gender="female")
        else:
            res = names.get_full_name()
        await ctx.response.send_message(embed=discord.Embed(title="Random Name", description=res, colour=self.bot.primary_colour))

    @app_commands.command(name="ign", description="Get an in game name")
    async def ign(self, ctx):
        res = namegenerator.gen()
        await ctx.response.send_message(embed=discord.Embed(title="Random Game Name", description=res, colour=self.bot.primary_colour))

    '''
    @app_commands.command(name="wheel", description="@someone but more dramatic")
    async def wheel(self, ctx, *, msg: str = ""):
        await ctx.guild.chunk()
        async with self.bot.pool.acquire() as conn:
            row = await conn.fetchrow("SELECT * FROM data WHERE guild=$1", ctx.guild.id)
        if row and row["ping"] is not None and row["ping"] == 1:
            canping = 1
        else:
            canping = 0
        potential = []
        async for i in ctx.guild.fetch_members(limit=None):
            if not i.bot:
                potential.append(i)
        finals = []
        for i in range(random.randint(2, 8)):
            user = random.choice(potential)
            await ctx.response.send_message(f"\N{ROUND PUSHPIN} {user.name}#{user.discriminator} chosen for the draw.")
            finals.append(user)
            await asyncio.sleep(10)
        user = random.choice(potential)
        if canping:
            await ctx.response.send_message(f"Final winner: {random.choice(finals).mention}")
        else:
            embed = discord.Embed(
                description=f"Final winner: {random.choice(finals).mention}", colour=self.bot.primary_colour
            )
            embed.set_footer(text=f"Use /toggleping to toggle between actually pinging the user")
            await ctx.response.send_message(embed=embed)
    '''
    @app_commands.command(name="card", description="Draw a random poker card")
    async def card(self, ctx):
        c = await self.bot.fetch_guild(623564336052568065)
        await c.chunk()
        cards = c.emojis
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
        await ctx.response.send_message(
            embed=discord.Embed(title="Card chosen", description=p1 + "\n" + p2, colour=self.bot.config.primary_colour)
        )

    @app_commands.command(name="somerole", description="Ping a user with that role in your server")
    async def somerole(self, ctx, role: str = ""):
        await ctx.guild.chunk()
        role = await converters.PingRole().convert(ctx, role)
        row = await self.bot.get_data(ctx.guild.id)
        if row and row["ping"] is not None and row["ping"] == 1:
            canping = 1
        else:
            canping = 0
        users = []
        
        async for member in ctx.guild.fetch_members(limit=None):
            if role in member.roles:
                users.append(member)
        user = random.choice(users)
        if canping:
            await ctx.response.send_message("Picked <@!{}> ({}#{})".format(user.id, user.name, user.discriminator))
        else:
            embed = discord.Embed(description="Picked <@!{}> ({}#{})".format(user.id, user.name, user.discriminator))
            await ctx.response.send_message(embed=embed)

    @app_commands.command(name="someroledm", description="Dm a user with that role in your server")
    async def someroledm(self, ctx, role: str):
        await ctx.guild.chunk()
        role = await converters.PingRole().convert(ctx, role)
        row = await self.bot.get_data(ctx.guild.id)
        if row and row["ping"] is not None and row["ping"] == 1:
            canping = 1
        else:
            canping = 0
        users = []
        async for member in ctx.guild.fetch_members(limit=None):
            if role in member.roles:
                users.append(member)
        user = random.choice(users)
        try:
            await user.send(f"You have been chosen in {ctx.guild.name} for the someroledm command!")
        except:
            await ctx.response.send_message("Are you sure that you allowed dms?")


    @app_commands.command(name="8ball", description="classic 8ball")
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
        await ctx.response.send_message(embed=discord.Embed(description=":8ball: " + random.choice(li), colour=self.bot.primary_colour))
    # TODO: Make coins from all countries
    @app_commands.command(name="coinflip", description="Flip a coin")
    async def coinflip(self, ctx):
        notland = random.randint(1, 6000)
        if notland == 1:
            await ctx.response.send_message(
                embed=discord.Embed(
                    description="The coin landed perfectly on it's side! What a miracle!",
                    colour=self.bot.primary_colour,
                )
            )

        guild = self.bot.get_guild(725303414220914758)
        heads = [e for e in guild.emojis if e.name == "washingtonheads"][0]
        tails = [e for e in guild.emojis if e.name == "washingtontails"][0]
        await ctx.response.send_message(str(random.choice([heads, tails])))

    @app_commands.command(name="dice", description="Throw a 6 side dice!")
    async def dice(self, ctx):
        res = random.randint(1, 6)
        guild = self.bot.get_guild(725303414220914758)
        emoji = [e for e in guild.emojis if e.name == f"dice{res}"][0]
        await ctx.response.send_message(emoji)
    @app_commands.command(name="d20", description="Throw a 20 sided dice.")
    async def d20(self, ctx):
        await ctx.response.send_message(file=discord.File(f"cogs/d20/dice{random.randint(1,20)}.png"))

    @app_commands.command(name="shuffle", description="Shuffle a list, separated with comma")
    async def shuffle(self, ctx, *, args: str):
        args=args.split(",")
        random.shuffle(args)
        res = ""
        for i in args:
            res += i + " "
        await ctx.response.send_message(embed=discord.Embed(title="Shuffled List", description=f"{res}", colour=self.bot.primary_colour))

    @app_commands.command(
        name="iamveryrandom",
        description="Randomly ban/kick a user. Person calling this command must have permissions.",
    )
    async def iamveryrandom(self, ctx, kick_or_ban: str = "ban"):
        await ctx.guild.chunk()
        if kick_or_ban.lower() != "ban" and kick_or_ban.lower() != "kick":
            await ctx.response.send_message("Do you want me to ban or kick?")
            return
        member = ctx.user
        auth = 0
        data=await self.bot.get_data(ctx.guild.id)
        for r in ctx.user.roles:
            if data['byebyeroles'] is not None and r.id in data['byebyeroles']:
                auth = 1
        if kick_or_ban.lower() == "ban" and not member.guild_permissions.ban_members and not auth:
            raise commands.MissingPermissions(["ban_members"])
        if kick_or_ban.lower() == "kick" and not member.guild_permissions.kick_members and not auth:
            raise commands.MissingPermissions(["kick_members"])

        guildmembers = []
        async for i in ctx.guild.fetch_members(limit=None):
            guildmembers.append(i)
        user = random.choice(guildmembers)
        await ctx.response.send_message("Picked <@!{}> ({}#{})".format(user.id, user.name, user.discriminator))
        webhook = ctx.followup
        print(webhook)

        await webhook.send("Say your goodbyes...")
        if kick_or_ban.lower() == "ban":

            await webhook.send("Banning in 10 seconds... ")
            await self.bot.change_presence(activity=discord.Game("Banning someone"))
            await asyncio.sleep(10)
            await self.bot.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.watching,   name=f"Now with better uptime and slash commands!"
                )
            )
            try:
                await ctx.channel.guild.ban(
                    user,
                    reason=f"Random ban requested by {ctx.author.name}#{ctx.author.discriminator}",
                    delete_message_days=0,
                )
            except Exception:
                await webhook.send("I need higher perms than that person.")
                return
            await webhook.send("Goodbye!")
        else:
            await webhook.send("Kicking in 10 seconds... ")
            await self.bot.change_presence(activity=discord.Game("Kicking someone"))
            await asyncio.sleep(10)
            await self.bot.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.watching,  name=f"Now with better uptime and slash commands!"
                )
            )
            try:
                await ctx.channel.guild.kick(
                    user,
                    reason=f"Random kick requested by {ctx.author.name}#{ctx.author.discriminator}",
                )
            except Exception:
                await webhook.send("I need higher perms than that person.")
                return
            await webhook.send("Goodbye!")

    @app_commands.command(
        name="team",
        description="Assign random teams players",
    )
    async def teams(self, ctx, num: typing.Optional[int] = 2, *, players:str):
        players=players.split(" ")
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
        await ctx.response.send_message(embed=embed)

    # TODO: fix this
    '''
    @app_commands.command(name="makegame", description="make a mafia like mystery game where each player will be assigned a role")
    async def makegame(self, ctx):
        await ctx.guild.chunk()
        def check(msg):
            return msg.author.id == ctx.author.id and msg.channel.id == ctx.channel.id
        botmsg = await ctx.response.send_message(embed=discord.Embed(description="React to this message to join the game!", colour=self.bot.config.primary_colour))
        await botmsg.add_reaction("✅")
        cd = await ctx.response.send_message(10*'◻️')
        for i in range(9,-1,-1):
            await asyncio.sleep(1)
            await ctx.response.edit_message(content=i*'◻️'+(10-i)*'◼️')
        cache_msg = discord.utils.get(self.bot.cached_messages, id=botmsg.id) 
        users=[]
        for i in cache_msg.reactions:
            li = await i.users().flatten()
            for i in li:
                if i.id != self.bot.user.id:
                    users.append(i.id)
        users=list(set(users))
        roles=[]
        while len(roles) != len(users):
            await ctx.response.send_message(f"Input the roles separated with ,  .Input {len(users)} roles for all players! (The same user that made the game)")
            rep = await self.bot.wait_for("message", timeout=60, check=check)
            rep=rep.content
            try:
                roles=rep.split(',')
            except:
                roles=[rep]
        random.shuffle(roles)
        random.shuffle(users)
        for i in range(len(roles)):
            try:
                await self.bot.get_user(users[i]).send(f"You were chosen to be the {roles[i]}")
            except:
                await ctx.response.send_message("Are you sure you allowed dms?")
    '''
    @app_commands.command(name="spintax", description="use spintax in random.bot! (example here: https://spintaxtool.appspot.com/")
    async def spintaxcmd(self, ctx, *, spintxt:str):
        await ctx.response.send_message(spintax.spin(spintxt))

    # TODO: fix this
    @app_commands.command(name="filechoose", description="Choose but reads the input from attachments. each option must be separated by a new line")
    async def filechoose(self, ctx):
        f=await ctx.message.attachments[0].read()
        chosen=random.choice(f.decode('utf-8').split('\n'))
        await ctx.response.send_message(embed=discord.Embed(description="The wheel has chosen **{}**!".format(chosen), colour=self.bot.primary_colour))

    @app_commands.command(name="password",description="Random password")
    async def pwmct(self, ctx, num:int=3):
        fp=open("cogs/freqwords.txt","r")
        everything=fp.read().split('\n')
        x = random.sample(everything, num)
        first = x[0][0].upper()+ x[0][1:]
        chosen = [first] + x[1:]
        chosen = "".join(chosen)
        for i in range(3):
            chosen+=str(random.randint(1,9))
        await ctx.response.send_message(f"{chosen}")


async def setup(bot):
    await bot.add_cog(Random(bot))
