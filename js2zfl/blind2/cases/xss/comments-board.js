const express = require('express');
const pool = require('./lib/db');

const app = express();
app.use(express.urlencoded({ extended: false }));

app.post('/board/comments', async (req, res) => {
  await pool.query('INSERT INTO comments (author, body) VALUES ($1, $2)', [
    req.body.author,
    req.body.body,
  ]);
  res.redirect('/board');
});

app.get('/board', async (req, res) => {
  const { rows } = await pool.query('SELECT author, body FROM comments ORDER BY id DESC LIMIT 50');
  let html = '<h1>Board</h1>';
  for (const row of rows) {
    html += `<div class="comment"><b>${row.author}</b><p>${row.body}</p></div>`;
  }
  res.send(html);
});

module.exports = app;
