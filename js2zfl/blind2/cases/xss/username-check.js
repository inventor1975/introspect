const express = require('express');

const app = express();

const USERNAME = /^[A-Za-z0-9_]+/;

app.get('/signup/check', (req, res) => {
  const username = req.query.username || '';
  if (!USERNAME.test(username)) {
    return res.status(400).send('<p>Usernames may contain letters, digits and underscores.</p>');
  }
  res.send(`<p>The name <em>${username}</em> is available.</p>`);
});

module.exports = app;
