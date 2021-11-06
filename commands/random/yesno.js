const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageEmbed } = require('discord.js');

module.exports = {
    data: new SlashCommandBuilder()
    .setName('yesno')
    .setDescription('Says yes or no'),
  info: {
    module: 'general',
    permLevel: 0,
    usage: 'help [command]'
  },
  async execute(interaction) {
    Array.prototype.sample = function(){
        return this[Math.floor(Math.random()*this.length)];
      }

    await interaction.reply({
      embeds: [
        new MessageEmbed()
          .setColor(process.env.BOT_PRIMARY_COLOUR)
          .setDescription(`${["yes!","no."].sample()}`)
      ]
    });
  }
};
