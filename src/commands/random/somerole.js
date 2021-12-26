const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageEmbed } = require('discord.js');
const { sample } = require('../../utils/tools');

module.exports = {
  data: new SlashCommandBuilder()
    .setName('somerole')
    .setDescription('Ping a random user in your server.')
    .addStringOption(option =>
      option.setName('role').setDescription('Ping the role').setRequired(true)
    )
    .addIntegerOption(option =>
      option.setName('number').setDescription('Enter number of users to ping').setRequired(false)
    ),
  info: {
    module: 'random',
    permLevel: 0,
    usage: 'someone [number of people]'
  },
  async execute(interaction) {
    const roleoption = interaction.options.getString('role');
    console.log(roleoption);
    const role =
      interaction.guild.roles.cache.find(thisRole => roleoption === thisRole.name) ||
      interaction.guild.roles.cache.find(thisRole => roleoption.includes(thisRole.id));
    console.log(role);
    const number = interaction.options.getInteger('number') || 1;
    let total = (await interaction.guild.members.fetch()).filter(member => !member.user.bot);
    console.log(total);
    for (let i of total) {
      console.log(i.roles.cache.size);
      if (i.roles.cache.size) console.log(i.roles, i.roles.cache.has(role.id));
    }
    total = total.filter(member => member.roles.cache.size >= 1 && member.roles.cache.has(role.id));
    console.log(total);
    const users = total.map(member => member.user);
    const pingedUsers = [];
    for (let i = 0; i < number; i++) {
      const user = sample(users);
      pingedUsers.push(user);
      users.splice(users.indexOf(user), 1);
    }
    const res = pingedUsers.map(user => `<@${user.id}>`).join('\n');
    console.log(res);
    const embed = new MessageEmbed()
      .setColor(process.env.BOT_PRIMARY_COLOUR)
      .setTitle('Chosen users')
      .setDescription(res);
    await interaction.reply({
      embeds: [embed]
    });
  }
};
