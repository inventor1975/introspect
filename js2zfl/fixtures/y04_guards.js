const ALLOWED = new Set(['a', 'b']);
app.get('/g', (req, res) => {
  let t = req.query.t;
  if (!ALLOWED.has(t)) { t = 'a'; }
  res.send('<p>' + t + '</p>');                          // clean: reset to a constant
  const c = req.query.c;
  if (!/^[a-z]+$/.test(c)) { return res.status(400).end(); }
  res.send('<p>' + c + '</p>');                          // clean: anchored
  const d = req.query.d;
  if (!/#[0-9a-f]{6}/.test(d)) { return res.status(400).end(); }
  res.send('<p>' + d + '</p>');                          // EXPECT: REFUTED (unanchored: anything can follow)
});
