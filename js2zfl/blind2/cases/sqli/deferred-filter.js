'use strict';

const express = require('express');
const mysql = require('mysql2');

const router = express.Router();
const pool = mysql.createPool({ database: 'analytics' });

// Mutable module-level state written by one route, read by another.
const lastFilter = { value: '1=1' };

router.post('/filter', (req, res) => {
  lastFilter.value = req.body.expression;
  res.sendStatus(202);
});

router.get('/run', (req, res) => {
  const sql = 'SELECT id, name FROM segments WHERE ' + lastFilter.value;
  pool.query(sql, (err, rows) => {
    if (err) return res.sendStatus(500);
    res.json(rows);
  });
});

module.exports = router;
