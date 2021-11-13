const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageEmbed } = require('discord.js');
const { sample } = require('../../utils/tools');

module.exports = {
  data: new SlashCommandBuilder()
    .setName('someone')
    .setDescription('Ping a random user in your server.')
    .addIntegerOption(option =>
      option
        .setName('number')
        .setDescription('Enter number of users to ping')
        .setRequired(false)
    ),
  info: {
    module: 'random',
    permLevel: 0,
    usage: 'someone [number of people]'
  },
  async execute(interaction) {
    const number = interaction.options.getInteger('number') || 1; 
    console.log(interaction.guild.members);
    const total  = interaction.guild.members.cache.filter(member => !member.user.bot)
    const users = total.map(member => member.user);
    const pingedUsers = [];
    for (let i = 0; i < number; i++) {
        const user = sample(users);
        pingedUsers.push(user);
        users.splice(users.indexOf(user), 1);
    }
    const res = pingedUsers.map(user => `<@${user.id}>`).join('\n')
    console.log(res);
    const embed = new MessageEmbed()
        .setColor(process.env.BOT_PRIMARY_COLOUR)
        .setTitle('Chosen users')
        .setDescription(res);
    await interaction.reply({
      embeds: [
        embed
      ]
      
    });
    }
};
