'use strict';

const express = require('express');
const mysql = require('mysql2');

const router = express.Router();
const conn = mysql.createConnection({ database: 'docs' });

router.get('/scan', (req, res) => {
  const keyword = req.query.keyword;
  // mysql2 escape() quotes and escapes for the SQL string context.
  const safe = conn.escape(keyword);
  const sql = 'SELECT id, title FROM documents WHERE title LIKE ' + safe;
  conn.query(sql, (err, rows) => {
    if (err) return res.sendStatus(500);
    res.json(rows);
  });
});

module.exports = router;
