import express from 'express';
import pg from 'pg';

const router = express.Router();
const pool = new pg.Pool({ connectionString: process.env.PG_URL });

router.get('/checkout/total', async (req, res) => {
  const cartId = Number(req.query.cart);
  if (!Number.isInteger(cartId)) {
    return res.status(400).json({ error: 'bad cart id' });
  }
  const result = await pool.query(
    'SELECT SUM(price * qty) AS total FROM cart_items WHERE cart_id = $1',
    [cartId]
  );
  res.json({ total: result.rows[0].total });
});

export default router;
