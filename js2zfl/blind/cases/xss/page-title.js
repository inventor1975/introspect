const express = require('express');

const app = express();

app.get('/docs', (req, res) => {
  const title = 'Documentation';
  const recent = [];
  if (req.query.from) {
    const title = req.query.from;
    recent.push(title.length);
    console.log('docs visited from', title);
  }
  res.send(`<html><head><title>${title}</title></head><body><h1>${title}</h1><p>${recent.length} referrals</p></body></html>`);
});

module.exports = app;
