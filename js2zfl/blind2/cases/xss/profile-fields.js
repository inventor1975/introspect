const express = require('express');

const app = express();
app.use(express.urlencoded({ extended: true }));

app.post('/profile/review', (req, res) => {
  const fields = new Map();
  for (const key of ['displayName', 'city', 'website']) {
    if (req.body[key]) {
      fields.set(key, req.body[key]);
    }
  }
  res.set('Content-Type', 'text/html');
  res.write('<dl>');
  fields.forEach((value, key) => {
    res.write(`<dt>${key}</dt><dd>${value}</dd>`);
  });
  res.end('</dl>');
});

module.exports = app;
