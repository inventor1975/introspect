const express = require('express');
const pug = require('pug');

const app = express();

const renderShout = pug.compile('div.shout\n  span.author= author\n  p!= message');

app.get('/shoutbox/preview', (req, res) => {
  res.send(renderShout({ author: req.query.author || 'anon', message: req.query.message || '' }));
});

module.exports = app;
