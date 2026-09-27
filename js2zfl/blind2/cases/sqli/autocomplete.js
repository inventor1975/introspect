'use strict';

const Router = require('@koa/router');
const mysql = require('mysql2/promise');

const router = new Router();
const pool = mysql.createPool({ database: 'directory' });

router.get('/autocomplete', async (ctx) => {
  const term = ctx.query.term;
  // Wildcards are added to the bound value, not to the statement text.
  const pattern = term + '%';
  const sql = 'SELECT city FROM cities WHERE city LIKE ? LIMIT 10';
  const [rows] = await pool.query(sql, [pattern]);
  ctx.body = rows.map((r) => r.city);
});

module.exports = router;
