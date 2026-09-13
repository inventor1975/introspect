const he = require('he');
module.exports = (req, res) => {
  const q = req.query.q;
  res.send(he.encode(q));   // clean: escaped for xss
  res.send(q);              // EXPECT: REFUTED [xss]
};
