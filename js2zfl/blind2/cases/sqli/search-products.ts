import { Router, Request, Response } from 'express';
import { Pool } from 'pg';

const router = Router();
const pool = new Pool({ connectionString: process.env.DATABASE_URL });

router.get('/products/search', async (req: Request, res: Response) => {
  const name = String(req.query.name ?? '');
  const text =
    "SELECT id, name, price FROM products WHERE name ILIKE '%" + name + "%'";
  const result = await pool.query(text);
  res.json(result.rows);
});

export default router;
