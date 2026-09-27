'use strict';

const express = require('express');
const cookieParser = require('cookie-parser');
const mysql = require('mysql2');

const app = express();
app.use(cookieParser());
const conn = mysql.createConnection({ database: 'app' });

app.get('/prefs', (req, res) => {
  const locale = req.cookies.locale;
  const sql =
    "SELECT key_name, value FROM prefs WHERE locale = '" + locale + "'";
  conn.query(sql, (err, rows) => {
    if (err) return res.sendStatus(500);
    res.json(rows);
  });
});

module.exports = app;
