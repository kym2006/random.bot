const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageEmbed } = require('discord.js');
const paginationEmbed = require('../../utils/paginator');

module.exports = {
  data: new SlashCommandBuilder()
    .setName('help')
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

    const commands = {};
    console.log('test')
    // eslint-disable-next-line no-return-assign
    interaction.client.modules.forEach(module => {
      commands[module] = [];
    });

    interaction.client.commands.forEach(cmd => {
      if (cmd.info.permLevel > 0) return;
      console.log(cmd.info.module)
      commands[cmd.info.module].push(`\`${cmd.data.name}\` ${cmd.data.description}`);
    });

    const allEmbeds = [];

    const embed = new MessageEmbed()
      .setColor(process.env.BOT_PRIMARY_COLOUR)
      .setTitle(`${interaction.client.user.username} help menu`)
      .setDescription('See more information on a command with `/help [command]`')
      .setThumbnail(interaction.client.user.displayAvatarURL());

    allEmbeds.push(embed);

    Object.keys(commands).forEach(category => {
      if (commands[category].length === 0) return;

      allEmbeds.push(
        new MessageEmbed()
          .setColor(process.env.BOT_PRIMARY_COLOUR)
          .setTitle(category.charAt(0).toUpperCase() + category.slice(1))
          .setDescription(commands[category].join('\n'))
          .setAuthor(`${interaction.client.user.username} help menu`)
          .setThumbnail(interaction.client.user.displayAvatarURL())
      );
    });

    paginationEmbed(interaction, allEmbeds);
  }
};
