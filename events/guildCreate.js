const { MessageEmbed } = require('discord.js');

module.exports = async (bot, guild) => {
  const guildCount = bot.guilds.cache.size;

  bot.channels.fetch(process.env.JOIN_CHANNEL).then(channel => {
    channel.send({
      embeds: [
        new MessageEmbed()
          .setColor(`#${process.env.BOT_SUCCESS_COLOUR}`)
          .setTitle('Server Join')
          .setDescription(`${guild.name} (${guild.id})`)
          .setFooter(`${guildCount} servers`)
          .setTimestamp()
      ]
    });
  });

  bot.user.setActivity(`randomness on ${guildCount} servers`, {
    type: 'PLAYING'
  });

  const firstChannel = guild.channels.cache.find(
    channel =>
      channel.type === 'GUILD_TEXT' &&
      channel.permissionsFor(guild.me).has('VIEW_CHANNEL') &&
      channel.permissionsFor(guild.me).has('SEND_MESSAGES') &&
      channel.permissionsFor(guild.me).has('EMBED_LINKS')
  );

  firstChannel.send({
    embeds: [
      new MessageEmbed()
        .setColor(`#${process.env.BOT_PRIMARY_COLOUR}`)
        .setDescription(
          'Thank you for inviting random.bot! Join our support server at ' +
            'https://discord.gg/ZatYnsX if you need help. The bot uses slash commands. ' +
            'Type /commands for a brief menu of all the commands, or /help for a more detailed version.'
        )
    ]
  });
};
