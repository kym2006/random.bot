const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageEmbed } = require('discord.js');
const { sample } = require('../../utils/tools');

function randomColour() {
  return '#' + Math.floor(Math.random() * 16777215).toString(16);
}

module.exports = {
  data: new SlashCommandBuilder().setName('colour').setDescription('Get a random colour'),

  info: {
    module: 'random',
    permLevel: 0,
    usage: 'colour'
  },
  async execute(interaction) {
    //get a random RGB colour
    const colour = randomColour();
    const embed = new MessageEmbed()
      .setColor(colour)
      .setTitle('Colour')
      .setDescription(`${colour}`);

    console.log(embed);
    await interaction.reply(embed);
  }
};
