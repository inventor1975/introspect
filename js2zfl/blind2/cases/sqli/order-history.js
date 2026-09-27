'use strict';

const Router = require('@koa/router');
const mysql = require('mysql2/promise');

const router = new Router();
const pool = mysql.createPool({ database: 'shop' });

router.get('/orders/history', async (ctx) => {
  const customer = ctx.query.customer;
  const sql =
    'SELECT order_id, total, placed_at FROM orders WHERE customer_ref = "' +
    customer +
    '" ORDER BY placed_at DESC';
  const [rows] = await pool.query(sql);
  ctx.body = rows;
});

module.exports = router;
