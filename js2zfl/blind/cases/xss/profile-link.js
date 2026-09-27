const express = require('express');
const escapeHtml = require('escape-html');

const app = express();

app.get('/u/:handle', (req, res) => {
  const handle = escapeHtml(req.params.handle);
  const website = escapeHtml(req.query.website || '#');
  res.send(`
    <div class="profile">
      <h2>@${handle}</h2>
      <a rel="nofollow" href="${website}">Personal website</a>
    </div>`);
});

module.exports = app;
