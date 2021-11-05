module.exports = async (bot, interaction) => {
  if (!interaction.isCommand()) return;

  const command = bot.commands.get(interaction.commandName);

  if (!command) return;

  try {
    command.execute(interaction);
  } catch (error) {
    process.stderr.write(error);

    interaction.reply({
      content: 'There was an error while executing this command!',
      ephemeral: true
    });
  }
};
