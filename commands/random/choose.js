const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageEmbed } = require('discord.js');

module.exports = {
    data: new SlashCommandBuilder()
    .setName('choose')
    .setDescription('Choose random element')
    .addStringOption(option => option.setName('choices').setDescription('Enter a choices, seperated by space')),
  info: {
    module: 'general',
    permLevel: 0,
    usage: 'help [command]'
  },
  async execute(interaction) {

    Array.prototype.sample = function(){
        return this[Math.floor(Math.random()*this.length)];
      }
    const choices = interaction.options.getString('choices').split(" ");
    await interaction.reply({
      embeds: [
        new MessageEmbed()
          .setColor(process.env.BOT_PRIMARY_COLOUR)
          .setDescription(`${choices.sample()}`)
      ]
    });
  }
};
