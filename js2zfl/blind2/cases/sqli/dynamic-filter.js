'use strict';

const express = require('express');
const mysql = require('mysql2');

const router = express.Router();
const pool = mysql.createPool({ database: 'catalog' });

router.get('/search', (req, res) => {
  const filters = req.query; // { color: 'red', size: 'L', ... }
  const clauses = [];
  for (const key of Object.keys(filters)) {
    clauses.push(key + " = '" + filters[key] + "'");
  }
  const where = clauses.length ? 'WHERE ' + clauses.join(' AND ') : '';
  const sql = 'SELECT id, name FROM products ' + where;
  pool.query(sql, (err, rows) => {
    if (err) return res.sendStatus(500);
    res.json(rows);
  });
});

module.exports = router;
