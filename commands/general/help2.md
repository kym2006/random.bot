const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageEmbed } = require('discord.js');
const {
  CommandInteraction,
  MessageActionRow,
  MessageButton,
  MessageSelectMenu,
  SelectMenuInteraction,
} = require("discord.js");
const paginationEmbed = require('../../utils/paginator');


module.exports = {
  
  data: new SlashCommandBuilder()
    .setName('help2')
    .setDescription('Shows the help menu or information for a specific command when specified.')
    .addStringOption(option =>
      option.setName('command').setDescription('Enter the command you need help for')
    ),
  info: {
    module: 'general',
    permLevel: 0,
    usage: 'help [command]'
  },
  async execute(interaction) {
    
    const command = interaction.options.getString('command');

    if (command) {
      const cmd = interaction.client.commands.get(command);

      if (!cmd) {
        interaction.reply({
          embeds: [
            new MessageEmbed()
              .setColor(process.env.BOT_ERROR_COLOUR)
              .setDescription(
                `Command \`${command}\` does not exist. Use \`/help\` to see all the commands.`
              )
          ]
        });

        return;
      }

      const embed = new MessageEmbed()
        .setColor(process.env.BOT_PRIMARY_COLOUR)
        .setTitle(cmd.data.name)
        .setDescription(cmd.data.description)
        .setFields([{ name: 'Usage', value: `\`\`\`${cmd.info.usage}\`\`\`` }]);

      interaction.reply({ embeds: [embed] });

      return;
    }
    options = ["hi"]
    page = "main"
    const row = new MessageActionRow().addComponents(
        new MessageSelectMenu()
            .setCustomId("help-main")
            .setPlaceholder(page === "main" ? "Initial landing page" : page)
            .addOptions(options)
    );
    const [inviteButton, topGGVote, supportServer] = getLinks();
    const row2 = new MessageActionRow().addComponents(
        inviteButton,
        topGGVote,
        supportServer
    );
    await interaction.reply({
      components: [row, row2],
    })
  }
};
