const cp = require('child_process');
module.exports = (req, res) => {
  const name = req.query.name;              // source
  cp.exec(`echo ${name}`);                  // EXPECT: REFUTED [shell] (template literal)
};
