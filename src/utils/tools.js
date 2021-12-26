const fs = require('fs');

function loadCommands(bot) {
  fs.readdirSync('./commands')
    .filter(folder => !folder.startsWith('.'))
    .forEach(folder => {
      bot.modules.push(folder);

      fs.readdirSync(`./commands/${folder}`)
        .filter(file => file.endsWith('.js'))
        .forEach(file => {
          delete require.cache[require.resolve(`../commands/${folder}/${file}`)];
          // eslint-disable-next-line
          const command = require(`../commands/${folder}/${file}`);

          bot.commands.set(command.data.name, command);
        });
    });
}

function loadEvents(bot) {
  fs.readdirSync('./events')
    .filter(file => file.endsWith('.js'))
    .forEach(file => {
      delete require.cache[require.resolve(`../events/${file}`)];
      // eslint-disable-next-line
      const event = require(`../events/${file}`);

      bot.removeAllListeners(file.split('.')[0]);
      bot.on(file.split('.')[0], event.bind(null, bot));
    });
}

exports.initBot = async bot => {
  loadCommands(bot);
  loadEvents(bot);
};

exports.sample = arr => {
  const index = Math.floor(Math.random() * arr.length);
  return arr[index];
};
