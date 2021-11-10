/* eslint-disable no-param-reassign */
const { SlashCommandBuilder } = require('@discordjs/builders');
const { inspect } = require('util');
const { MessageEmbed } = require('discord.js');

module.exports = {
  data: new SlashCommandBuilder()
    .setName('eval')
    .setDescription('Evaluate code.')
    .addStringOption(option =>
      option.setName('code').setDescription('Enter the code to evaluate').setRequired(true)
    ),
  info: {
    module: 'owner',
    permLevel: 10,
    usage: 'eval <code>'
  },
  async execute(interaction) {
    const code = interaction.options.getString('code');

    // eslint-disable-next-line no-eval
    await eval(`(async () => { ${code} })()`)
      .then(evaled => {
        if (typeof evaled !== 'string') {
          evaled = inspect(evaled);
        }

        evaled = evaled
          .replace(new RegExp(interaction.client.token, 'g'), '--TOKEN--')
          .replace(new RegExp('`', 'g'), `\`${String.fromCharCode(8203)}`);

        interaction.reply({
          embeds: [
            new MessageEmbed()
              .setColor(process.env.BOT_PRIMARY_COLOUR)
              .setDescription(`\`\`\`js\n${evaled.substr(0, 2000)}\n\`\`\``)
          ],
          ephemeral: true
        });
      })
      .catch(err => {
        interaction.reply({
          embeds: [
            new MessageEmbed()
              .setColor(process.env.BOT_ERROR_COLOUR)
              .setTitle('⚠ Error')
              .setDescription(`\`\`\`js\n${err.toString().substr(0, 2000)}\n\`\`\``)
          ],
          ephemeral: true
        });
      });
  }
};
