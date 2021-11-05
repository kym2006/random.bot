const fs = require('fs');
const { REST } = require('@discordjs/rest');
const { Routes } = require('discord-api-types/v9');
require('dotenv').config();

const commands = [];

fs.readdirSync('./commands')
  .filter(folder => !folder.startsWith('.'))
  .forEach(folder =>
    fs
      .readdirSync(`./commands/${folder}`)
      .filter(file => file.endsWith('.js'))
      // eslint-disable-next-line
      .forEach(file => commands.push(require(`./commands/${folder}/${file}`).data.toJSON()))
  );

const rest = new REST({ version: '9' }).setToken(process.env.BOT_TOKEN);

rest
  // .put(Routes.applicationCommands(process.env.CLIENT_ID), { body: commands })
  .put(Routes.applicationGuildCommands(process.env.CLIENT_ID, process.env.SERVER_ID), {
    body: commands
  })
  .then(() => process.stdout.write('Successfully registered application commands.\n'))
  .catch(process.stderr.write);
