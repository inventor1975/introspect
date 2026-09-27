'use strict';

const express = require('express');
const sqlite3 = require('sqlite3');

const app = express();
const db = new sqlite3.Database('./forum.db');

app.get('/threads/:slug/comments', (req, res) => {
  const slug = req.params.slug;
  const sql =
    "SELECT author, body, created_at FROM comments WHERE thread_slug = '" +
    slug + "' ORDER BY created_at ASC";
  db.all(sql, (err, rows) => {
    if (err) return res.status(500).end();
    res.json(rows);
  });
});

module.exports = app;
