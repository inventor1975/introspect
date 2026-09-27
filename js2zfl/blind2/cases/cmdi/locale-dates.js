const express = require('express');
const cookieParser = require('cookie-parser');
const { execSync } = require('child_process');

const app = express();
app.use(cookieParser());

app.get('/calendar/today', (req, res) => {
  const lang = req.cookies.lang || 'en_US';
  const formatted = execSync(`LC_TIME=${lang}.UTF-8 date '+%A %d %B %Y'`).toString().trim();
  res.json({ today: formatted });
});

module.exports = app;
