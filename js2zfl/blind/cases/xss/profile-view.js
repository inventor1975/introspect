const path = require('path');
const express = require('express');

const app = express();
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');

app.get('/profile', (req, res) => {
  const name = req.query.name || 'guest';
  const since = req.query.since || 'today';
  res.render('profile', { name, since });
});

module.exports = app;
