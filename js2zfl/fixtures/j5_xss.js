module.exports = (req, res) => {
  const p = req.params.id;                    // source
  res.send('<h1>' + p + '</h1>');             // EXPECT: REFUTED [xss]
};
