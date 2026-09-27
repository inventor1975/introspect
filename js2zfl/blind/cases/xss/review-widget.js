const express = require('express');
const { tidy, truncate } = require('./lib/text-utils');

const app = express();
app.use(express.json());

app.post('/reviews/render', (req, res) => {
  const title = tidy(req.body.title || 'Review');
  const text = tidy(truncate(req.body.text || '', 500));
  res.send(`<blockquote><h4>${title}</h4>${text}</blockquote>`);
});

module.exports = app;
