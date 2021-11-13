const { Client, Collection, Intents } = require('discord.js');
// const { Pool } = require('pg');
const { initBot } = require('./utils/tools');
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
// bot.pool = new Pool({ connectionString: process.env.DB_URL });

initBot(bot);

bot.login(process.env.BOT_TOKEN);
