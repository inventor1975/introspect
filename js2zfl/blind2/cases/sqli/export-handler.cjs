'use strict';

const express = require('express');
const mysql = require('mysql');

const router = express.Router();
const conn = mysql.createConnection({ database: 'warehouse' });

router.get('/export', (req, res) => {
  const table = req.query.table;
  const since = req.query.since;
  const sql =
    'SELECT * FROM ' + table + ' WHERE updated_at >= "' + since + '"';
  conn.query(sql, (err, rows) => {
    if (err) return res.status(500).send('export error');
    res.json(rows);
  });
});

module.exports = router;
