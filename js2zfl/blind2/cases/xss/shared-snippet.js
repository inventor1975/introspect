const express = require('express');

const app = express();

app.get('/snippet', (req, res) => {
  const encoded = req.query.s;
  if (!encoded) {
    return res.status(400).send('<p>Missing snippet.</p>');
  }
  const snippet = Buffer.from(decodeURIComponent(encoded), 'base64').toString('utf8');
  res.send('<div class="snippet">' + snippet + '</div>');
});

module.exports = app;
