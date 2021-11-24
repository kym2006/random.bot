const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageEmbed } = require('discord.js');
const { sample } = require('../../utils/tools');
function randint(x, y) {
    return Math.floor(Math.random() * (y - x + 1) + x);
}
module.exports = {
  data: new SlashCommandBuilder()
    .setName('randint')
    .setDescription('Choose a random number from x to y')
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
    const x = choices[0];
    const y = choices[1];

    const embed = new MessageEmbed()
      .setColor('#0099ff')
      .setTitle('Random number')
      .setDescription(`I chose **${randint(x,y)}**`);

    interaction.reply(embed);
  }
};
