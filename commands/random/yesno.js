const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageEmbed } = require('discord.js');
const { sample } = require('../../utils/tools');

module.exports = {
  data: new SlashCommandBuilder().setName('yesno').setDescription('Says yes or no.'),
  info: {
    module: 'random',
    permLevel: 0,
    usage: 'yesno'
  },
  async execute(interaction) {
    await interaction.reply({
      embeds: [
        new MessageEmbed()
          .setColor(process.env.BOT_PRIMARY_COLOUR)
          .setDescription(`${sample(['yes!', 'no.'])}`)
      ]
    });
  }
};
