const express = require('express');

const app = express();

function renderBanner() {
  const message = 'Scheduled maintenance on Sunday 02:00-04:00 UTC';
  return `<div class="banner">${message}</div>`;
}

app.get('/banner', (req, res) => {
  const message = req.query.message;
  if (message) {
    console.info('banner requested with custom message of length', message.length);
  }
  res.send(renderBanner(message));
});

module.exports = app;
