'use strict';

const express = require('express');
const Database = require('better-sqlite3');

const router = express.Router();
const db = new Database('tokens.db');
const findStmt = db.prepare(
  'SELECT user_id, scope FROM api_tokens WHERE token = ? AND revoked = 0'
);

router.get('/token/introspect', (req, res) => {
  const token = req.query.token;
  const row = findStmt.get(token);
  res.json({ active: Boolean(row), scope: row ? row.scope : null });
});

module.exports = router;
