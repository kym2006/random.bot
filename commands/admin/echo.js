const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageEmbed } = require('discord.js');

module.exports = {
  data: new SlashCommandBuilder()
    .setName('echo')
    .setDescription('Make me say something.')
    .addStringOption(option =>
      option.setName('message').setDescription('Enter the message to be echoed').setRequired(true)
    )
    .addChannelOption(option =>
      option.setName('channel').setDescription('Enter the channel to echo in')
    ),
  info: {
    module: 'admin',
    permLevel: 9,
    usage: 'echo [channel] <message>'
  },
  async execute(interaction) {
    interaction.reply({
      embeds: [
        new MessageEmbed()
          .setColor(process.env.BOT_PRIMARY_COLOUR)
          .setDescription('Echoing message...')
      ],
      ephemeral: true
    });

    const channel = interaction.options.getChannel('channel') || interaction.channel;
    const message = interaction.options.getString('message');

    await channel.send(message);
  }
};
