'use strict';

const express = require('express');
const mysql = require('mysql2');
const escapeHtml = require('escape-html');

const router = express.Router();
const conn = mysql.createConnection({ database: 'legacy' });

router.get('/legacy/search', (req, res) => {
  const term = req.query.q;
  // HTML-escaping does nothing for SQL string context.
  const safeTerm = escapeHtml(term);
  const sql =
    "SELECT id, title FROM documents WHERE title LIKE '%" + safeTerm + "%'";
  conn.query(sql, (err, rows) => {
    if (err) return res.sendStatus(500);
    res.json(rows);
  });
});

module.exports = router;
