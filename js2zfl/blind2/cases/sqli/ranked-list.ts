import { Router, Request, Response } from 'express';
import { Pool } from 'pg';

const router = Router();
const pool = new Pool();

const SORT_COLUMNS: Record<string, string> = {
  recent: 'created_at DESC',
  popular: 'votes DESC',
  title: 'title ASC',
};

router.get('/posts', async (req: Request, res: Response) => {
  const order = SORT_COLUMNS[String(req.query.sort)] ?? 'created_at DESC';
  const text = `SELECT id, title, votes FROM posts ORDER BY ${order} LIMIT 50`;
  const result = await pool.query(text);
  res.json(result.rows);
});

export default router;
