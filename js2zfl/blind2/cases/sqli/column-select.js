'use strict';

const express = require('express');
const mysql = require('mysql2');

const router = express.Router();
const pool = mysql.createPool({ database: 'crm' });

const ALLOWED = { name: 'name', email: 'email', company: 'company' };

router.get('/contacts/by', (req, res) => {
  const field = ALLOWED[req.query.field];
  if (!field) return res.status(400).json({ error: 'unknown field' });
  const value = req.query.value;
  const sql = 'SELECT id, name FROM contacts WHERE ' + field + ' = ?';
  pool.query(sql, [value], (err, rows) => {
    if (err) return res.sendStatus(500);
    res.json(rows);
  });
});

module.exports = router;
