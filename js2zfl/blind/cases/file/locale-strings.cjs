'use strict';
const express = require('express');
const cookieParser = require('cookie-parser');
const fs = require('fs');
const path = require('path');

const LOCALES = path.join(__dirname, 'locales');
const app = express();
app.use(cookieParser());

app.get('/i18n/strings', (req, res) => {
  const lang = req.cookies.lang || 'en';
  const file = path.join(LOCALES, lang + '.json');
  let strings;
  try {
    strings = JSON.parse(fs.readFileSync(file, 'utf8'));
  } catch (e) {
    strings = JSON.parse(fs.readFileSync(path.join(LOCALES, 'en.json'), 'utf8'));
  }
  res.set('Cache-Control', 'private, max-age=300').json(strings);
});

module.exports = app;
