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
  const row2 = new MessageActionRow().addComponents(inviteButton, topGGVote, supportServer);
  const time = 120000;

  let page = 0;

  if (interaction.deferred === false) {
    await interaction.deferReply();
  }

  const curPage = await interaction.editReply({
    embeds: [pages[page].setFooter(`Page ${page + 1} / ${pages.length}`)],
    components: [row, row2],
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
      components: [row, row2]
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
        components: [disabledRow, row2]
      });
    }
  });

  return curPage;
};

module.exports = paginationEmbed;
