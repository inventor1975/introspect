import { Router, Request, Response } from 'express';
import { createConnection } from 'mysql2';

const router = Router();
const conn = createConnection({ database: 'gateway' });

router.get('/route', (req: Request, res: Response) => {
  const key = req.headers['x-api-key'] as string;
  if (!/^[a-f0-9]{32}$/.test(key || '')) {
    return res.status(401).json({ error: 'invalid key' });
  }
  const sql = 'SELECT tier, quota FROM api_keys WHERE key_hash = ?';
  conn.query(sql, [key], (err, rows) => {
    if (err) return res.sendStatus(500);
    res.json(rows[0] || {});
  });
});

export default router;
