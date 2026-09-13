const cp = require('child_process');
const allow = new Set(['ls', 'pwd']);
module.exports = (req, res) => {
  const cmd = req.query.cmd;
  if (!allow.has(cmd)) { return; }   // negated membership guard + early return
  cp.exec(cmd);                       // EXPECT: nothing (validated above)
};
