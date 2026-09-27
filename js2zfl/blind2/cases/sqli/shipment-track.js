'use strict';

const Router = require('@koa/router');
const mysql = require('mysql2/promise');

const router = new Router();
const pool = mysql.createPool({ database: 'logistics' });

router.get('/shipments/:tracking', async (ctx) => {
  const tracking = ctx.params.tracking;
  const sql =
    'SELECT status, last_seen, carrier FROM shipments WHERE tracking_no = ?';
  const [rows] = await pool.query(sql, [tracking]);
  ctx.body = rows[0] || {};
});

module.exports = router;
