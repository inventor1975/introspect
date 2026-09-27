const express = require('express');
const pug = require('pug');

const app = express();

const alertBox = pug.compile([
  'div.alert(class="alert-" + kind)',
  '  strong= heading',
  '  p= text',
].join('\n'));

app.get('/alert', (req, res) => {
  const kind = ['info', 'warning', 'error'].includes(req.query.kind) ? req.query.kind : 'info';
  res.send(alertBox({ kind, heading: 'Notice', text: req.query.text }));
});

module.exports = app;
