'use strict';

const express = require('express');
const mysql = require('mysql2');

const router = express.Router();
const conn = mysql.createConnection({ database: 'app' });

router.get('/dashboard', (req, res) => {
  const mode = req.query.mode;
  // Branch selects between two fixed statements; input never enters SQL text.
  const sql =
    mode === 'admin'
      ? 'SELECT * FROM stats_admin'
      : 'SELECT * FROM stats_public';
  conn.query(sql, (err, rows) => {
    if (err) return res.sendStatus(500);
    res.json(rows);
  });
});

module.exports = router;
