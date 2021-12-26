const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageEmbed } = require('discord.js');
const { sample } = require('../../utils/tools');

module.exports = {
  data: new SlashCommandBuilder().setName('card').setDescription('Get a random card.'),
  info: {
    module: 'random',
    permLevel: 0,
    usage: 'card'
  },
  async execute(interaction) {
    let suit = sample(['spade', 'heart', 'club', 'diamond']);
    let rank = sample(['2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '1']);
    var color;
    if (suit == 'spade' || suit == 'club') {
      color = 'BLACK';
    } else {
      color = 'RED';
    }
    suitemoji = interaction.client.emojis.cache.filter(emoji => emoji.name === suit).first();

    console.log('b' + rank.toString());
    if (color == 'BLACK') {
      rankemoji = interaction.client.emojis.cache
        .filter(emoji => emoji.name === 'b' + rank.toString())
        .first();
    } else {
      rankemoji = interaction.client.emojis.cache
        .filter(emoji => emoji.name === 'a' + rank.toString())
        .first();
    }
    interaction.reply(`${rankemoji}\n${suitemoji}`);
  }
};
