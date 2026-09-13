const cp = require('child_process');
const allow = ['ls', 'pwd'];
module.exports = (req, res) => {
  const cmd = req.query.cmd;
  if (allow.includes(cmd)) {
    cp.exec(cmd);                 // EXPECT: nothing (whitelist guard narrows cmd)
  }
  cp.exec(cmd);                   // EXPECT: REFUTED [shell] (unguarded, still tainted)
};
