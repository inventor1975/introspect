'use strict';

const Router = require('@koa/router');
const mysql = require('mysql2/promise');

const router = new Router();
const pool = mysql.createPool({ database: 'directory' });

router.get('/suggest', async (ctx) => {
  const prefix = ctx.query.prefix;
  const sql =
    "SELECT full_name FROM people WHERE full_name LIKE '" + prefix + "%' LIMIT 10";
  const [rows] = await pool.query(sql);
  ctx.body = rows.map((r) => r.full_name);
});

module.exports = router;
