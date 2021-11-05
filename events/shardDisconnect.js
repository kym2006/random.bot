const { MessageEmbed } = require('discord.js');

module.exports = async (bot, id) => {
  bot.channels.fetch(process.env.EVENT_CHANNEL).then(channel => {
    channel.send({
      embeds: [
        new MessageEmbed()
          .setColor(`#${process.env.BOT_PRIMARY_COLOUR}`)
          .setTitle(`Shard ${id} Disconnected`)
          .setTimestamp()
      ]
    });
  });
};
