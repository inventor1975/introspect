const express = require('express');
const fs = require('fs');
const path = require('path');

const settings = JSON.parse(fs.readFileSync(path.join(__dirname, 'config', 'site.json'), 'utf8'));

const app = express();

app.get('/', (req, res) => {
  const banner = settings.banners[req.query.lang] || settings.banners.en;
  res.send(`<div class="banner">${banner}</div><h1>${settings.siteName}</h1>`);
});

module.exports = app;
