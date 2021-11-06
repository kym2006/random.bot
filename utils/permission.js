const { admins, owners } = require('../index').bot;

module.exports = [
  {
    level: 0,
    check: () => true
  },
  {
    level: 9,
    check: message => admins.includes(message.author.id)
  },
  {
    level: 10,
    check: message => owners.includes(message.author.id)
  }
];
