const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageEmbed } = require('discord.js');
const { sample } = require('../../utils/tools');

module.exports = {
  data: new SlashCommandBuilder()
    .setName('choose')
    .setDescription('Choose a random element.')
    .addStringOption(option =>
      option
        .setName('choices')
        .setDescription('Enter choices seperated by a space')
        .setRequired(true)
    ),
  info: {
    module: 'random',
    permLevel: 0,
    usage: 'random <item 1> <item 2> ...'
  },
  async execute(interaction) {
    const choices = interaction.options.getString('choices').split(' ');
    await interaction.reply({
      embeds: [
        new MessageEmbed()
          .setColor(process.env.BOT_PRIMARY_COLOUR)
          .setDescription(`The wheel has chosen **${sample(choices)}**!`)
      ]
    });
  }
};
