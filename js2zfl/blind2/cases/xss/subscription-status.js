const express = require('express');

const app = express();

app.get('/subscription', (req, res) => {
  const subscribed = req.query.sub === 'yes';
  const plan = req.query.plan;
  const label = subscribed ? 'Subscribed' : 'Not subscribed';
  res.send(`<p class="${subscribed ? 'on' : 'off'}">${label}${plan ? ' (plan selected)' : ''}</p>`);
});

module.exports = app;
