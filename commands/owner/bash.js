const { SlashCommandBuilder } = require('@discordjs/builders');
const { exec } = require('child_process');
const { MessageEmbed } = require('discord.js');

module.exports = {
  data: new SlashCommandBuilder()
    .setName('bash')
    .setDescription('Execute code in bash.')
    .addStringOption(option =>
      option.setName('code').setDescription('Enter the code to execute').setRequired(true)
    ),
  info: {
    module: 'owner',
    permLevel: 10,
    usage: 'bash <code>'
  },
  async execute(interaction) {
    const code = interaction.options.getString('code');

    exec(code, (error, stdout, stderr) => {
      if (error) {
        interaction.reply({
          embeds: [
            new MessageEmbed()
              .setColor(process.env.BOT_ERROR_COLOUR)
              .setTitle('⚠ Error')
              .setDescription(`\`\`\`${error.toString().substr(0, 2000)}\`\`\``)
          ],
          ephemeral: true
        });

        return;
      }

      if (!stdout && !stderr) {
        interaction.reply({
          embeds: [
            new MessageEmbed()
              .setColor(process.env.BOT_PRIMARY_COLOUR)
              .setDescription('Nothing was returned.')
          ],
          ephemeral: true
        });

        return;
      }

      if (stdout) {
        interaction.reply({
          embeds: [
            new MessageEmbed()
              .setColor(process.env.BOT_PRIMARY_COLOUR)
              .setDescription(
                `\`\`\`bash\n${stdout
                  .replace(new RegExp('`', 'g'), `\`${String.fromCharCode(8203)}`)
                  .substr(0, 2000)}\`\`\``
              )
          ],
          ephemeral: true
        });
      }

      if (stderr) {
        interaction.reply({
          embeds: [
            new MessageEmbed()
              .setColor(process.env.BOT_ERROR_COLOUR)
              .setDescription(`\`\`\`${stderr.substr(0, 2000)}\`\`\``)
          ],
          ephemeral: true
        });
      }
    });
  }
};
