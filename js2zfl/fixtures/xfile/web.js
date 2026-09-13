const dao = require('./dao');
module.exports = (req, res, db) => {
  const id = req.query.id;
  dao.q(db, id);                              // EXPECT: REFUTED cross-file (q param1 -> sql)
};
