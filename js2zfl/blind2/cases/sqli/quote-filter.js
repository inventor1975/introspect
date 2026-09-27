'use strict';

const express = require('express');
const mysql = require('mysql2');

const router = express.Router();
const pool = mysql.createPool({ database: 'blog' });

function stripQuotes(value) {
  // Only removes single quotes; backslash and other vectors survive.
  return String(value).replace(/'/g, '');
}

router.get('/posts/by-author', (req, res) => {
  const author = stripQuotes(req.query.author);
  const sql = "SELECT slug, title FROM posts WHERE author = '" + author + "'";
  pool.query(sql, (err, rows) => {
    if (err) return res.sendStatus(500);
    res.json(rows);
  });
});

module.exports = router;
