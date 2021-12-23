const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageEmbed } = require('discord.js');
const { sample } = require('../../utils/tools');

module.exports = {
  data: new SlashCommandBuilder().setName('coinflip').setDescription('Flip a coin! (click on the emoji to get the side'),
  info: {
    module: 'random',
    permLevel: 0,
    usage: 'coinflip'
  },

  async execute(interaction) {
    await interaction.reply({
        files: [sample(["https://cdn.discordapp.com/attachments/725303414665248853/923469163710787644/reverseyuan.jpg",
        "https://cdn.discordapp.com/attachments/725303414665248853/923469163933089822/obverseyuan.jpg"])]
    });
  }
};
