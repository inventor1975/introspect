module.exports = (req, res) => {
  const expr = req.query.expr;                // source
  eval(expr);                                 // EXPECT: REFUTED [code]
};
