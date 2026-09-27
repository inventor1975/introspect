const express = require('express');
const ejs = require('ejs');

const app = express();

const MAIL = [
  '<div class="mail">',
  '  <h1>Welcome, <%= firstName %>!</h1>',
  '  <p>Your plan: <%= plan %></p>',
  '</div>',
].join('\n');

app.get('/mail/welcome/preview', (req, res) => {
  const html = ejs.render(MAIL, {
    firstName: req.query.firstName || 'there',
    plan: req.query.plan || 'free',
  });
  res.send(html);
});

module.exports = app;
