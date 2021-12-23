const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageEmbed } = require('discord.js');
const { sample } = require('../../utils/tools');
const axios = require('axios');

module.exports = {
  data: new SlashCommandBuilder()
    .setName('user')
    .setDescription('Get a random (fake) person'),
  info: {
    module: 'random',
    permLevel: 0,
    usage: 'user'
  },
  async execute(interaction) {
    axios
    .get('https://randomuser.me/api/', {})
    .then(res => {
        console.log(res.data.results[0].name.first);
        const user = res.data.results[0]
        const embed = new MessageEmbed()

        .setColor(process.env.BOT_PRIMARY_COLOUR)
        .setTitle(`${user.name.first} ${user.name.last}`)
        .setDescription(`${user.email}`)
        .setThumbnail(user.picture.large)
        .setFooter(`${user.location.city}, ${user.location.state}`)
        .setTimestamp()
        .setURL(user.picture.large)
        .addField('Phone', user.phone, true)
        
        .addField('Address', `${user.location.street.number} ${user.location.street.name}`, true)
        .addField('City', `${user.location.city}, ${user.location.state} ${user.location.postcode}`, true)
        .addField('Country', `${user.location.country}`, true)
        .addField('Age', `${user.dob.age}`, true)
        //.addField('         
        
        interaction.reply({
            embeds: [
                embed
            ]
        }); 
    })
  }
};
