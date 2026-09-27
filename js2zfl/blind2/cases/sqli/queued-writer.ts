import { Router, Request, Response } from 'express';
import { createPool } from 'mysql2/promise';

const router = Router();
const pool = createPool({ database: 'jobs' });

// A module-level queue collects fragments across requests.
const pending: string[] = [];

router.post('/enqueue', (req: Request, res: Response) => {
  pending.push(req.body.name as string);
  res.sendStatus(202);
});

router.post('/flush', async (req: Request, res: Response) => {
  const values = pending.map((n) => `('${n}')`).join(', ');
  await pool.query('INSERT INTO tags (name) VALUES ' + values);
  pending.length = 0;
  res.sendStatus(200);
});

export default router;
