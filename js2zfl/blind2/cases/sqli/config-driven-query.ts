import { Router, Request, Response } from 'express';
import { Pool } from 'pg';

const router = Router();
const pool = new Pool();

router.get('/segment/:name', async (req: Request, res: Response) => {
  const name = req.params.name;
  // The predicate template is loaded from a settings table, not from the request.
  const cfg = await pool.query(
    'SELECT predicate FROM segment_defs WHERE name = $1',
    [name]
  );
  const predicate = cfg.rows[0]?.predicate ?? 'FALSE';
  const result = await pool.query(
    'SELECT id, email FROM members WHERE ' + predicate
  );
  res.json(result.rows);
});

export default router;
