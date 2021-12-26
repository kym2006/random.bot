const admins = process.env.BOT_ADMINS.split(',');
const owners = process.env.BOT_OWNERS.split(',');

module.exports = [
  {
    level: 0,
    check: () => true
  },
  {
    level: 9,
    check: user => admins.includes(user.id)
  },
  {
    level: 10,
    check: user => owners.includes(user.id)
  }
];
