'use strict';

const express = require('express');
const fs = require('fs');
const mysql = require('mysql2');

const router = express.Router();
const conn = mysql.createConnection({ database: 'reporting' });

router.get('/reports/:name', (req, res) => {
  const name = req.params.name;
  // The SQL body comes from an operator-maintained file on disk.
  const template = fs.readFileSync('./queries/' + name + '.sql', 'utf8');
  conn.query(template, (err, rows) => {
    if (err) return res.status(500).send('report error');
    res.json(rows);
  });
});

module.exports = router;
