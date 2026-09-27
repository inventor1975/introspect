const escapeHtml = require('escape-html');
app.get('/p', (req, res) => {
  res.send(`<p>${escapeHtml(req.query.q)}</p>`);                     // clean
  res.send(`<a href="${escapeHtml(req.query.u)}">go</a>`);           // EXPECT: REFUTED (javascript: survives)
  res.send('<a href="/s?q=' + encodeURIComponent(req.query.q) + '">s</a>');   // clean
});
