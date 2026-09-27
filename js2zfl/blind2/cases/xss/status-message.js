const express = require('express');
const pug = require('pug');

const app = express();

const renderStatus = pug.compile('div.status\n  span.who= who\n  p= message');

app.get('/status/message', (req, res) => {
  res.send(renderStatus({ who: req.query.who || 'system', message: req.query.message || '' }));
});

module.exports = app;
