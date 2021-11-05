const { MessageEmbed } = require('discord.js');

module.exports = async bot => {
  process.stdout.write(`${bot.user.username}#${bot.user.discriminator} is online!`);

  bot.channels.fetch(process.env.EVENT_CHANNEL).then(channel => {
    channel.send({
      embeds: [
        new MessageEmbed()
          .setColor(`#${process.env.BOT_SUCCESS_COLOUR}`)
          .setTitle('Bot Ready')
          .setTimestamp()
      ]
    });
  });

  bot.user.setActivity(`randomness on ${bot.guilds.cache.size} servers`, {
    type: 'PLAYING'
  });
};
