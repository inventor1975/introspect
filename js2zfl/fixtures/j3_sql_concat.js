module.exports = (req, res, db) => {
  const id = req.body.id;                     // source
  db.query('SELECT * FROM u WHERE id=' + id); // EXPECT: REFUTED [sql]
};
