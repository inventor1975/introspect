const cp = require('child_process');
module.exports = (req, res) => {
  const q = req.query;                       // Values object, not passed to a sink
  cp.exec('ls -la');                         // constant: EXPECT nothing
  res.send('static page');                   // constant: EXPECT nothing
};
