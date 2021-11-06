const { MessageActionRow, MessageButton } = require('discord.js');

const paginationEmbed = async (interaction, pages) => {
  const buttonList = [
    new MessageButton().setCustomId('firstPage').setEmoji('⏮️'),
    new MessageButton().setCustomId('previousPage').setEmoji('◀️'),
    new MessageButton().setCustomId('stop').setEmoji('⏹️'),
    new MessageButton().setCustomId('nextPage').setEmoji('▶️'),
    new MessageButton().setCustomId('lastPage').setEmoji('⏭️')
  ].map(button => button.setStyle('PRIMARY'));
  const row = new MessageActionRow().addComponents(buttonList);
  const time = 120000;

  let page = 0;

  if (interaction.deferred === false) {
    await interaction.deferReply();
  }

  const curPage = await interaction.editReply({
    embeds: [pages[page].setFooter(`Page ${page + 1} / ${pages.length}`)],
    components: [row],
    fetchReply: true
  });

  const filter = i => buttonList.map(b => b.customId).includes(i.customId);

  const collector = await curPage.createMessageComponentCollector({
    filter,
    time
  });

  collector.on('collect', async i => {
    switch (i.customId) {
      case buttonList[0].customId:
        page = 0;
        break;
      case buttonList[1].customId:
        page = page > 0 ? (page -= 1) : pages.length - 1;
        break;
      case buttonList[2].customId:
        collector.stop();
        await i.deferUpdate();
        return;
      case buttonList[3].customId:
        page = page + 1 < pages.length ? (page += 1) : 0;
        break;
      case buttonList[4].customId:
        page = pages.length - 1;
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
        buttonList.map(b => b.setDisabled(true))
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
