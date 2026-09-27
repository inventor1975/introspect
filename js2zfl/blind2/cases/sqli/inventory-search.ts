import { Router, Request, Response } from 'express';
import { Pool } from 'pg';

const router = Router();
const pool = new Pool();

router.get('/inventory', async (req: Request, res: Response) => {
  const warehouse = String(req.query.warehouse ?? '');
  const text =
    'SELECT sku, qty FROM inventory WHERE warehouse = $1 ORDER BY sku';
  const result = await pool.query(text, [warehouse]);
  res.json(result.rows);
});

export default router;
