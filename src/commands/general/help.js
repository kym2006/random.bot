const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageEmbed } = require('discord.js');
const paginationEmbed = require('../../utils/paginator');
function getLinks() {
  const inviteButton = new MessageButton()
    .setLabel('Invite the bot!')
    .setStyle('LINK')
    .setURL(
      'https://discord.com/api/oauth2/authorize?client_id=606402391314530319&permissions=526636809431&scope=bot%20applications.commands'
    );
  const topGGVote = new MessageButton()
    .setLabel('Vote (Top.gg)')
    .setStyle('LINK')
    .setURL('https://top.gg/bot/606402391314530319');
  const supportServer = new MessageButton()
    .setLabel('Support Server')
    .setStyle('LINK')
    .setURL('https://discord.gg/ZatYnsX');
  return [inviteButton, topGGVote, supportServer];
}
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
    interaction.client.modules.forEach(module => {
      commands[module] = [];
    });

    interaction.client.commands.forEach(cmd => {
      if (cmd.info.permLevel > 0) return;
      console.log(cmd.info.module);
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
