'use strict';

const express = require('express');
const mysql = require('mysql2');

const app = express();
const db = mysql.createPool({ database: 'social' });

app.get('/profile/:username', (req, res) => {
  const username = req.params.username;
  const query =
    "SELECT bio, avatar_url, joined_at FROM profiles WHERE username = '" +
    username +
    "'";
  db.query(query, (err, rows) => {
    if (err) return res.sendStatus(500);
    res.json(rows[0] || {});
  });
});

module.exports = app;
