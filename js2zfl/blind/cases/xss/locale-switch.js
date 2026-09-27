const express = require('express');

const app = express();

const SUPPORTED = ['en', 'de', 'fr', 'es'];

function resolveLocale(tag) {
  if (!SUPPORTED.includes(tag)) {
    throw new Error(`Unsupported locale "${tag}"`);
  }
  return tag;
}

app.get('/locale', (req, res) => {
  try {
    const locale = resolveLocale(req.query.lang);
    res.cookie('locale', locale);
    res.send('<p>Language updated.</p>');
  } catch (err) {
    res.status(400).send(`<p class="error">${err.message}</p>`);
  }
});

module.exports = app;
