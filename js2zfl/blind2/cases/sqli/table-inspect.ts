import { Router, Request, Response } from 'express';
import { createConnection } from 'mysql2';

const router = Router();
const conn = createConnection({ database: 'admin' });

router.get('/inspect', (req: Request, res: Response) => {
  const table = req.query.table as string;
  // escapeId quotes an identifier so it cannot break out of its position.
  const ident = conn.escapeId(table);
  const sql = 'SELECT COUNT(*) AS n FROM ' + ident;
  conn.query(sql, (err, rows) => {
    if (err) return res.sendStatus(500);
    res.json(rows);
  });
});

export default router;
