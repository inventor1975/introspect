const cp = require('child_process');
function runCmd(c) { cp.exec(c); }            // param -> shell (summary)
module.exports = (req, res) => {
  const cmd = req.query.cmd;
  runCmd(cmd);                                // EXPECT: REFUTED (cross-func summary)
  runCmd('safe');                             // EXPECT: clean
};
