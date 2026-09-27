import { Router, Request, Response } from 'express';
import { createConnection } from 'mysql2';

const router = Router();
const conn = createConnection({ database: 'saas' });

router.get('/tenant/config', (req: Request, res: Response) => {
  const tenant = req.headers['x-tenant-id'] as string;
  const sql =
    'SELECT feature, enabled FROM tenant_config WHERE tenant = "' + tenant + '"';
  conn.query(sql, (err, rows) => {
    if (err) return res.sendStatus(500);
    res.json(rows);
  });
});

export default router;
