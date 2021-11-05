const fs = require('fs');
const { Client, Collection, Intents } = require('discord.js');
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

fs.readdirSync('./commands')
  .filter(folder => !folder.startsWith('.'))
  .forEach(folder => {
    bot.modules.push(folder);

    fs.readdirSync(`./commands/${folder}`)
      .filter(file => file.endsWith('.js'))
      .forEach(file => {
        delete require.cache[require.resolve(`./commands/${folder}/${file}`)];
        // eslint-disable-next-line
        const command = require(`./commands/${folder}/${file}`);

        bot.commands.set(command.data.name, command);
      });
  });

fs.readdirSync('./events')
  .filter(file => file.endsWith('.js'))
  .forEach(file => {
    delete require.cache[require.resolve(`./events/${file}`)];
    // eslint-disable-next-line
    const event = require(`./events/${file}`);

    bot.removeAllListeners(file.split('.')[0]);
    bot.on(file.split('.')[0], event.bind(null, bot));
  });

bot.login(process.env.BOT_TOKEN);
