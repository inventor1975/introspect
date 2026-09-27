const express = require('express');
const { escapeHtml } = require('./lib/html');

const app = express();

app.get('/contacts/edit', (req, res) => {
  const name = req.query.name || '';
  const email = req.query.email || '';
  res.send(`
<form method="post" action="/contacts">
  <label>Name <input type="text" name="name" value="${escapeHtml(name)}"></label>
  <label>Email <input type="email" name="email" value="${escapeHtml(email)}"></label>
  <button type="submit">Save</button>
</form>`);
});

module.exports = app;
