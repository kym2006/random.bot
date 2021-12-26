const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageEmbed } = require('discord.js');

module.exports = {
  data: new SlashCommandBuilder().setName('commands').setDescription('Shows the command panel.'),
  info: {
    module: 'general',
    permLevel: 0,
    usage: 'commands'
  },
  async execute(interaction) {
    const commands = {};

    // eslint-disable-next-line no-return-assign
    interaction.client.modules.forEach(module => {
      commands[module] = [];
    });

    interaction.client.commands.forEach(cmd => {
      if (cmd.info.permLevel > 0) return;
      commands[cmd.info.module].push(cmd.data.name);
    });

    const embed = new MessageEmbed()
      .setColor(process.env.BOT_PRIMARY_COLOUR)
      .setTitle(`${interaction.client.user.username} command panel`)
      .setDescription('See all of my commands. Use /help for more information.')
      .setThumbnail(interaction.client.user.displayAvatarURL());

    const fields = [
      {
        name: 'Invite',
        value: `[Invite here](https://discord.com/oauth2/authorize?client_id=${process.env.CLIENT_ID}&scope=bot&applications.commands&permissions=519239)`
      },
      { name: 'Support Server', value: '[Join here](https://discord.gg/ZatYnsX)' },
      { name: 'Donate', value: '[Donate here](https://paypal.me/kym2k06)' }
    ];

    Object.keys(commands).forEach(category => {
      if (commands[category].length === 0) return;

      fields.push({
        name: category.charAt(0).toUpperCase() + category.slice(1),
        value: `\`\`\`\n${commands[category].join('\n')}\`\`\``
      });
    });

    embed.addFields(fields);

    interaction.reply({ embeds: [embed] });
  }
};
