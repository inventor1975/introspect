const path = require('path');
const express = require('express');

const app = express();
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');

app.get('/greet', (req, res) => {
  const message = req.query.message || 'Have a nice day!';
  res.render('greeting', { message });
});

module.exports = app;
