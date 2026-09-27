const util = require('util');
const express = require('express');

const app = express();

const NOTICE = '<div class="notice notice-%s">%s</div>';

app.get('/notice', (req, res) => {
  const level = req.query.level === 'warn' ? 'warn' : 'info';
  const html = util.format(NOTICE, level, req.query.message);
  res.send(html);
});

module.exports = app;
