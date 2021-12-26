const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageEmbed } = require('discord.js');
const { loadavg, cpus } = require('os');
const { duration } = require('moment');
require('moment-duration-format');
const { version, dependencies } = require('../../package.json');

module.exports = {
  data: new SlashCommandBuilder()
    .setName('stats')
    .setDescription('See some super cool statistics about me.'),
  info: {
    module: 'general',
    permLevel: 0,
    usage: 'stats'
  },
  async execute(interaction) {
    const embed = new MessageEmbed()
      .setColor(process.env.BOT_PRIMARY_COLOUR)
      .setTitle(`${interaction.client.user.username} statistics`)
      .setFields([
        {
          name: 'Owner',
          value: 'kym2006#6342\nwaterflamev8#4123',
          inline: true
        },
        {
          name: 'Bot Version',
          value: version,
          inline: true
        },
        {
          name: 'Uptime',
          value: duration(interaction.client.uptime).format('M[m] W[w] d[d] h[hr] m[m] s[s]'),
          inline: true
        },
        {
          name: 'Servers',
          value: `${interaction.client.guilds.cache.size}`,
          inline: true
        },
        {
          name: 'Users',
          value: `${interaction.client.users.cache.size}`,
          inline: true
        },
        {
          name: 'CPU Usage',
          value: `${Math.round((loadavg()[0] / cpus().length) * 1000) / 10}%`,
          inline: true
        },
        {
          name: 'RAM Usage',
          value: `${Math.round((process.memoryUsage().heapUsed / 1024 / 1024) * 10) / 10}MiB`,
          inline: true
        },
        {
          name: 'Node Version',
          value: process.version.slice(1),
          inline: true
        },
        {
          name: 'Discord.js Version',
          value: dependencies['discord.js'].slice(1),
          inline: true
        }
      ])
      .setThumbnail(interaction.client.user.displayAvatarURL())
      .setFooter(
        '</> with ❤ using Discord.js',
        'https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/javascript/javascript.png'
      );

    interaction.reply({ embeds: [embed] });
  }
};
