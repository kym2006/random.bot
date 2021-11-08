const { Client, Collection, Intents } = require('discord.js');
const { initCommands, initEvents } = require('./utils/tools');
require('dotenv').config();

const bot = new Client({
  shards: 'auto',
  allowedMentions: { parse: ['users', 'roles'] },
  intents: [
    Intents.FLAGS.GUILDS,
    Intents.FLAGS.GUILD_MEMBERS,
    Intents.FLAGS.GUILD_MESSAGES,
    Intents.FLAGS.DIRECT_MESSAGES
  ]
});

bot.commands = new Collection();
bot.modules = [];

initCommands(bot);
initEvents(bot);

bot.login(process.env.BOT_TOKEN);