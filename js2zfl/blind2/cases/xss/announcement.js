const express = require('express');
const { layout } = require('./lib/html');

const app = express();

app.get('/announce', (req, res) => {
  const message = req.query.msg;
  const body = '<div class="announce">' + message + '</div>';
  res.send(layout('Announcement', body));
});

module.exports = app;
