const express = require('express');
const escapeHtml = require('escape-html');

const app = express();

app.get('/find', (req, res) => {
  const q = escapeHtml(req.query.q || '');
  res.send(`
    <form action='/find' method='get'>
      <input type='search' name='q' value='${q}'>
      <button>Search</button>
    </form>
    <p>No results for '${q}'.</p>`);
});

module.exports = app;
