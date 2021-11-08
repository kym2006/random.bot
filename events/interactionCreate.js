const { MessageEmbed } = require('discord.js');
const permission = require('../utils/permission');

module.exports = async (bot, interaction) => {
  if (!interaction.isCommand()) return;

  const command = bot.commands.get(interaction.commandName);

  if (!command) return;

  let permLevel = 0;
  const permOrder = permission.slice(0).sort((a, b) => (a.level < b.level ? 1 : -1));

  while (permOrder.length) {
    const perm = permOrder.shift();
    if (perm.check(interaction.user)) {
      permLevel = perm.level;
      break;
    }
  }

  if (permLevel < command.info.permLevel) {
    interaction.reply({
      embeds: [
        new MessageEmbed()
          .setColor(process.env.BOT_ERROR_COLOUR)
          .setTitle('Permission Denied')
          .setDescription('You do not have permission to use this command.')
      ],
      ephemeral: true
    });
    return;
  }

  command.execute(interaction).catch(error => {
    interaction.reply({
      embeds: [
        new MessageEmbed()
          .setColor(process.env.BOT_ERROR_COLOUR)
          .setTitle('Command Error')
          .setDescription(`Please report this in the support server.\n\`\`\`${error}\`\`\``)
      ],
      ephemeral: true
    });
  });
};
