const { MessageEmbed } = require('discord.js');

module.exports = async (bot, guild) => {
  const guildCount = bot.guilds.cache.size;

  bot.channels.fetch(process.env.JOIN_CHANNEL).then(channel => {
    channel.send({
      embeds: [
        new MessageEmbed()
          .setColor(`#${process.env.BOT_ERROR_COLOUR}`)
          .setTitle('Server Leave')
          .setDescription(`${guild.name} (${guild.id})`)
          .setFooter(`${guildCount} servers`)
          .setTimestamp()
      ]
    });
  });

  bot.user.setActivity(`randomness on ${guildCount} servers`, {
    type: 'PLAYING'
  });
};
