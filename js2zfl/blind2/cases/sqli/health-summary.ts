import { Router, Request, Response } from 'express';
import { Pool } from 'pg';

const router = Router();
const pool = new Pool();

router.get('/health', async (req: Request, res: Response) => {
  // The caller-supplied verbosity only controls logging, never the query.
  const verbose = req.query.verbose === '1';
  if (verbose) console.log('health check requested');
  const result = await pool.query(
    'SELECT COUNT(*) AS sessions FROM active_sessions'
  );
  res.json({ sessions: result.rows[0].sessions });
});

export default router;
