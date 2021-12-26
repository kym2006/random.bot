const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageEmbed } = require('discord.js');
const { initBot } = require('../../utils/tools');

module.exports = {
  data: new SlashCommandBuilder().setName('reload').setDescription('Reload the bot.'),
  info: {
    module: 'admin',
    permLevel: 9,
    usage: 'reload'
  },
  async execute(interaction) {
    interaction.reply({
      embeds: [
        new MessageEmbed()
          .setColor(process.env.BOT_PRIMARY_COLOUR)
          .setDescription('Reloading bot...')
      ],
      ephemeral: true
    });

    initBot(interaction.client);
  }
};
