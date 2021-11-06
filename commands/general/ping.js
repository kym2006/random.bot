const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageEmbed } = require('discord.js');

module.exports = {
  data: new SlashCommandBuilder().setName('ping').setDescription('Pong! Get my latency.'),
  info: {
    module: 'general',
    permLevel: 0,
    usage: 'ping'
  },
  async execute(interaction) {
    const startTime = Date.now();

    await interaction.reply({
      embeds: [
        new MessageEmbed()
          .setColor(process.env.BOT_PRIMARY_COLOUR)
          .setDescription('Checking latency...')
      ]
    });

    interaction.editReply({
      embeds: [
        new MessageEmbed()
          .setColor(process.env.BOT_PRIMARY_COLOUR)
          .setTitle('Pong!')
          .setDescription(
            `Gateway latency: ${interaction.client.ws.ping}ms.\nHTTP API Latency: ${Math.round(
              Date.now() - startTime
            )}ms.`
          )
      ]
    });
  }
};
