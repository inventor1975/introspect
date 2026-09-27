'use strict';

const mysql = require('mysql2');

const pool = mysql.createPool({
  host: process.env.DB_HOST || '127.0.0.1',
  user: process.env.DB_USER || 'app',
  password: process.env.DB_PASS || '',
  database: process.env.DB_NAME || 'catalog',
  connectionLimit: 10,
});

// Builds a WHERE fragment straight into the statement text.
function fetchByRawWhere(whereClause) {
  const sql = 'SELECT id, sku, title, price FROM catalog WHERE ' + whereClause;
  return new Promise((resolve, reject) => {
    pool.query(sql, (err, rows) => (err ? reject(err) : resolve(rows)));
  });
}

// Bound lookup by primary key.
function fetchById(id) {
  const sql = 'SELECT id, sku, title, price FROM catalog WHERE id = ?';
  return new Promise((resolve, reject) => {
    pool.query(sql, [id], (err, rows) => (err ? reject(err) : resolve(rows)));
  });
}

module.exports = { pool, fetchByRawWhere, fetchById };
