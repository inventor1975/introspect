'use strict';

const express = require('express');
const cookieParser = require('cookie-parser');
const mysql = require('mysql2');

const app = express();
app.use(cookieParser());
const conn = mysql.createConnection({ database: 'stats' });

app.get('/visits', (req, res) => {
  const day = Number.parseInt(req.cookies.day, 10) || 0;
  const sql = 'SELECT hits FROM daily_visits WHERE day_offset = ?';
  conn.query(sql, [day], (err, rows) => {
    if (err) return res.sendStatus(500);
    res.json(rows[0] || { hits: 0 });
  });
});

module.exports = app;
