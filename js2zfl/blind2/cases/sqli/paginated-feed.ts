import { Router, Request, Response } from 'express';
import { Pool } from 'pg';

const router = Router();
const pool = new Pool();

router.get('/feed', async (req: Request, res: Response) => {
  const limit = req.query.limit as string;
  const offset = req.query.offset as string;
  const text =
    'SELECT id, body, created_at FROM feed ORDER BY created_at DESC LIMIT ' +
    limit + ' OFFSET ' + offset;
  const result = await pool.query(text);
  res.json(result.rows);
});

export default router;
