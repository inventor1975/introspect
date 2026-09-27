const escapeHtml = require('escape-html');
const ALLOWED = new Set(['a', 'b']);
app.get('/c', (req, res) => {
  const tags = [].concat(req.query.t);
  res.send('<ul>' + tags.filter(t => ALLOWED.has(t)).join('') + '</ul>');     // clean
  res.send('<ul>' + tags.map(escapeHtml).join('') + '</ul>');                // clean
  res.send(tags.map(t => [t, 1]));                                           // clean: an array is JSON
  res.send('<ul>' + tags.map(t => '<li>' + t + '</li>').join('') + '</ul>'); // EXPECT: REFUTED
});
