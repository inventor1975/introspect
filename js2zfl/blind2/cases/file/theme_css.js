const express = require('express');
const cookieParser = require('cookie-parser');
const path = require('path');

const app = express();
app.use(cookieParser());

const THEMES_DIR = path.join(__dirname, 'public', 'themes');

app.get('/theme.css', (req, res) => {
  const theme = req.cookies.theme || 'light.css';
  res.set('Cache-Control', 'private, max-age=300');
  res.sendFile(path.join(THEMES_DIR, theme), (err) => {
    if (err) {
      res.sendFile(path.join(THEMES_DIR, 'light.css'));
    }
  });
});

module.exports = app;
