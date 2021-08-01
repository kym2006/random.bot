import topgg
from discord.ext import commands
# This example uses topggpy's webhook system.
# The port must be a number between 1024 and 49151.
from discord.ext import commands

import config


class Topgg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.topgg_webhook = topgg.WebhookManager(bot).dbl_webhook("/dblwebhook", "password")
        self.bot.topgg_webhook.run(5000)  # this method can be awaited as well

    @commands.Cog.listener()
    async def on_dbl_vote(data):
        if data["type"] == "test":
        # this is roughly equivalent to
        # return await on_dbl_test(data) in this case
            print(data)

        print(f"Received a vote:\n{data}")

    @commands.Cog.listener()
    async def on_dbl_test(data):

        print(f"Received a test vote:\n{data}")


def setup(bot):
    bot.add_cog(Topgg(bot))


