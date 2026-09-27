const express = require('express');

const app = express();

const THEMES = ['light', 'dark', 'high-contrast'];

app.get('/preferences/theme', (req, res) => {
  let theme = req.query.theme;
  if (!THEMES.includes(theme)) {
    theme = 'light';
  }
  res.send(`<body class="theme-${theme}"><p>Theme set to ${theme}.</p></body>`);
});

module.exports = app;
