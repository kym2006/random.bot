import datetime
import logging

import discord
from discord.ext import commands
import random 
log = logging.getLogger(__name__)


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        ctx = await self.bot.get_context(message)
        if not ctx.command:
            return
        if message.guild:
            permissions = message.channel.permissions_for(message.guild.me)
            if permissions.send_messages is False:
                return
            elif permissions.embed_links is False:
                await message.channel.send("The Embed Links permission is needed for basic commands to work.")
                return
        if ctx.command.cog_name in ["Owner", "Admin"] and (
            ctx.author.id in self.bot.config.admins or ctx.author.id in self.bot.config.owners
        ):
            embed = discord.Embed(
                title=ctx.command.name.title(),
                description=ctx.message.content,
                colour=self.bot.primary_colour,
                timestamp=datetime.datetime.utcnow(),
            )
            embed.set_author(name=f"{ctx.author} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
            if self.bot.config.admin_channel:
                await self.bot.fetch_channel(self.bot.config.admin_channel).send(embed=embed.to_dict())
        r = random.randint(1, 69696)
        if r == 1:
            await ctx.response.send_message(f"⭐Ad 1 Scene 1⭐Hey {ctx.author.name}! We've been trying to reach YOU concerning your vehicle's extended warranty. You should've received a notice in the mail about your car's extended warranty eligibility. Since we've not gotten a response, we're giving you a final courtesy call before we close out your file. Donate 2 https://paypal.me/kym2k06 to be removed and placed on our do-not-call list. To speak to someone about possibly extending or reinstating your vehicle's warranty, press https://discord.gg/ZatYnsX to speak with a warranty specialist.")
        elif r == 2:
            await ctx.response.send_message(f"⭐Ad 1 Scene 2⭐Hey {ctx.author.name}! Here's some bubble wrap for YOU! ||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pay||||pal||||.me||||/ky||||m2k||||06||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||||pop||")
        elif r == 3:
            await ctx.response.send_message(f"⭐Ad 1 Scene 3⭐Hey {ctx.author.name}! I heard you like emojis, so here are some for you! .--. .- -.-- .--. .- .-.. .-.-.- -- . -..-. -.- -.-- -- ..--- -.- ----- -....")
        elif r == 4:
            await ctx.response.send_message(f"⭐Ad 1 Scene 4⭐🚨DIFFICULT AD🚨Hey {ctx.author.name}! Well I heard you like hidden things or something, so here's a flareon for you! https://cdn.discordapp.com/attachments/811929798259245066/858593138301861898/radicalisedflareon.png")
        elif r == 5:
            await ctx.response.send_message(f'''⭐Ad 1 Scene 5⭐Hey {ctx.author.name}! 
            Finally, one I can answer! I literally have never been able to answer any askreddit question in my entire life, and have never posted anything on reddit until this exact moment that is happening right now.

Writing this on mobile, sorry for bad formatting, also english is my 6th language so there might be one wrong word, TLDR at the bottom. Obligatory not a teacher, but my sister's friend's stepbrother's boss's daughter's friend's mom's cousin's dog's breeder's brother's coworker's father's youtube channel had a comment where some guy talked about a post he saw on tumblr that referenced an instagram post from this one girl who posted on reddit and had a comment where there was this guy who knew this guy who knew this guy who knew this guy who knew this guy who knew this guy who knew this guy who knew this guy who knew this guy who knew this guy who knew this guy who knew this guy who knew this guy who knew this guy's cousin who was friends with a girl who's mom was a teacher. Anyways she said that A bot one time turned in an ad instead of a dank meme. Haha!

TL;DR - A bot one time turned in an ad instead of a dank meme. Haha!

Edit: Wow, thank you so much for the upvotes! I've never gotten more than 10 before!

Edit 2: WOW! I hit 100 upvotes, thank you guys!

Edit 6: Speling) 

Edit 7: Included my paypal(https://paypal.me/kym2k06). Not trying to ask for donations or anything... ''')

        elif r==6:
            await ctx.response.send_message(f'''⭐Ad 1 Scene 6⭐Hey {ctx.author.name}! I sexually Identify as the "I sexually identify as https://paypal.me/kym2k06" joke. Ever since I was a child, I've dreamed of flippantly dismissing any concepts or discussions regarding gender that don't fit in with what I learned in 8th grade bio. People say to me that this joke hasn't been funny since 2014 and please at least come up with a new one, but I don't care, I'm hilarious. I'm having a plastic surgeon install Ctrl, C, and V keys on my body. From now on I want you guys to call me "epic kek dank meme trannies owned with facts and logic" and respect my right to shit up social media. If you can't accept me you're a memeophobe and need to check your ability-to-critically-think privilege. Thank you for being so understanding.)''')
        

        elif r==7:
            await ctx.response.send_message(f'''⭐Ad 1 Scene 7⭐Hey {ctx.author.name}! The Girl you just called fat? She shit herself & lost 15kgs. The Boy you just called stupid? He shit himself. The Girl you just called ugly? She spends hours shitting and farting. The Boy you just tripped? He shit his pants. There`s more to people than you think. Donate to https://paypal.me/kym2k06 if your against bullying.''')

        elif r==8:
            await ctx.response.send_message(f'''⭐Ad 1 Scene 8⭐Hey {ctx.author.name}! We just matched on Instagram! Check out my account! OFFICIAL ACCOUNT!

BLM, ACAB

she/her•13 💁♥️ • 2-9-06 💋💞 • Atheist 😈💫 • God's Princess 😇🙏• Twerker 😵🍑 • aquarius ♒• DON'T MESSED WITH ME 😏✨ • Jake 😍💕 Paypal: https://paypal.me/kym2k06''')
        elif r==9:
            await ctx.response.send_message(f'''⭐Ad 1 Scene 9⭐Hey {ctx.author.name}! This 👈👉 is money snek(https://paypal.me/kym2k06) 🐍🐍💰💰 Upsnek ⬆⬆🔜🔜 in 7.123 snekonds 🐍🐍 or you ✋✋ will NEVER ❌❌❌❌ get monies 💰💰 again Beware!! ✋✋❌❌ You😏😏 don't ❌❌ have much time!!🕛🕧🕐🕜🕑🕝🕝 You 😏😏 may never ❌❌get monies 💰💰🐍💰💰 again!!''')
        elif r==10:
            await ctx.response.send_message(f'''⭐Ad 1 Scene 10⭐Hey {ctx.author.name}! You may be thinking, why are all the ads stolen off of reddit and the likes? Well this is because, the creator of the bot doesn't have the time to make high quality ads himself. If you would like to change this, consider donating to https://paypal.me/kym2k06''')
        elif r>=11 and r <= 20:
            await ctx.response.send_message(f'''⭐Ad 1 Scene 11⭐Hey Please vote for the bot please vote for the bot please vote for the bot https://top.gg/bot/606402391314530319/vote if not bot will not grow then i can't host it anymore cmon at least i'm better than ea games''')
        
        
        await self.bot.invoke(ctx)

    '''
    @commands.Cog.listener()
    async def on_command(self, ctx):
        if str(ctx.command) in self.bot.down_commands:
            await ctx.response.send_message(embed=discord.Embed(description="That command is down right now. Join the [support server](https://discord.gg/ZatYnsX) and read the announcements to find out why. We are already working on a fix :)"))
            return 
        if ctx.command.cog_name in ["Owner", "Admin"] and (
            ctx.author.id in self.bot.config.admins or ctx.author.id in self.bot.config.owners
            ):
            embed = discord.Embed(
                title=ctx.command.name.title(),
                description=ctx.message.content,
                colour=self.bot.primary_colour,
                timestamp=datetime.datetime.utcnow(),
            )
            embed.set_author(name=f"{ctx.author} ({ctx.author.id})", icon_url=ctx.author.avatar_url)

            await self.bot.get_channel(self.bot.config.admin_channel).send(embed=embed)
    '''
        
        
    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.tree.copy_global_to(guild=(await self.bot.fetch_guild(725303414220914758)))
        await self.bot.tree.sync(guild=(await self.bot.fetch_guild(725303414220914758)))
        embed = discord.Embed(
            title="Bot Ready",
            colour=0x00FF00,
            timestamp=datetime.datetime.utcnow(),
        )
        
        await (await self.bot.fetch_channel(self.bot.config.event_channel)).send(embed=embed)
        await self.bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching, name=f"Astra inclinant, sed non obligant."
            )
        )

    @commands.Cog.listener()
    async def on_shard_ready(self, shard):
        embed = discord.Embed(
            title=f"Shard {shard} Ready",
            colour=0x00FF00,
            timestamp=datetime.datetime.utcnow(),
        )
        c = await self.bot.fetch_channel(self.bot.config.event_channel)
        await c.send(embed=embed)

    @commands.Cog.listener()
    async def on_shard_connect(self, shard):
        embed = discord.Embed(
            title=f"Shard {shard} Connected",
            colour=0x00FF00,
            timestamp=datetime.datetime.utcnow(),
        )
        c = await self.bot.fetch_channel(self.bot.config.event_channel)
        await c.send(embed=embed)

    @commands.Cog.listener()
    async def on_shard_disconnect(self, shard):
        embed = discord.Embed(
            title=f"Shard {shard} Disconnected",
            colour=0xFF0000,
            timestamp=datetime.datetime.utcnow(),
        )
        c = await self.bot.fetch_channel(self.bot.config.event_channel)
        await c.send(embed=embed)

    @commands.Cog.listener()
    async def on_shard_resumed(self, shard):
        embed = discord.Embed(
            title=f"Shard {shard} Resumed",
            colour=self.bot.config.primary_colour,
            timestamp=datetime.datetime.utcnow(),
        )
        c = await self.bot.fetch_channel(self.bot.config.event_channel)
        await c.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        content = f"New guild: {guild.name}! Now at **{len(self.bot.guilds)}** guilds!"
        c = await self.bot.fetch_channel(self.bot.config.join_channel)
        await c.send(content=content, allowed_mentions=discord.AllowedMentions.none())
        txtchannel = await self.bot.fetch_channel(self.bot.config.join_channel)
        await guild.chunk()
        for i in guild.channels:
            if i.type == txtchannel.type:
                try:
                    await i.send(
                        embed=discord.Embed(
                            description="""Thank you for inviting random.bot! Join our support server at https://discord.gg/ZatYnsX if you need help.
The default prefix for the bot is ?, but you can change it with the prefix command.
Type ?commands for a brief menu of all the commands, or ?help for a more detailed version.""",
                            colour=self.bot.primary_colour,
                        )
                    )
                    return
                except:
                    continue

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
       content = f"Guild leave: {guild.name}... Now at **{len(self.bot.guilds)}** guilds"
       c = await self.bot.fetch_channel(self.bot.config.join_channel)
       await c.send(content=content,allowed_mentions=discord.AllowedMentions.none())


async def setup(bot):
    await bot.add_cog(Events(bot))
