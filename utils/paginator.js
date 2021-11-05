const { MessageActionRow, MessageButton } = require('discord.js');

const paginationEmbed = async (interaction, pages) => {
  const buttonList = [new MessageButton().setLabel('◀')];
  const row = new MessageActionRow().addComponents(buttonList);

  let page = 0;

  if (interaction.deferred === false) {
    await interaction.deferReply();
  }

  const curPage = await interaction.editReply({
    embeds: [pages[page].setFooter(`Page ${page + 1} / ${pages.length}`)],
    components: [row],
    fetchReply: true
  });

  const filter = i =>
    i.customId === buttonList[0].customId || i.customId === buttonList[1].customId;

  const collector = await curPage.createMessageComponentCollector({
    filter,
    time: timeout
  });

  collector.on('collect', async i => {
    switch (i.customId) {
      case buttonList[0].customId:
        page = page > 0 ? --page : pages.length - 1;
        break;
      case buttonList[1].customId:
        page = page + 1 < pages.length ? ++page : 0;
        break;
      default:
        break;
    }
    await i.deferUpdate();
    await i.editReply({
      embeds: [pages[page].setFooter(`Page ${page + 1} / ${pages.length}`)],
      components: [row]
    });
    collector.resetTimer();
  });

  collector.on('end', () => {
    if (!curPage.deleted) {
      const disabledRow = new MessageActionRow().addComponents(
        buttonList[0].setDisabled(true),
        buttonList[1].setDisabled(true)
      );
      curPage.edit({
        embeds: [pages[page].setFooter(`Page ${page + 1} / ${pages.length}`)],
        components: [disabledRow]
      });
    }
  });

  return curPage;
};
module.exports = paginationEmbed;
