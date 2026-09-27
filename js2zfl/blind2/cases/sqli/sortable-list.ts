import { Router, Request, Response } from 'express';
import { createPool } from 'mysql2/promise';

const router = Router();
const pool = createPool({ database: 'crm' });

router.get('/contacts', async (req: Request, res: Response) => {
  const sortBy = String(req.query.sort || 'name');
  const dir = String(req.query.dir || 'asc');
  const sql = `SELECT id, name, company FROM contacts ORDER BY ${sortBy} ${dir}`;
  const [rows] = await pool.query(sql);
  res.json(rows);
});

export default router;
