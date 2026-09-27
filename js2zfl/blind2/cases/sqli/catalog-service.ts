import { Router, Request, Response } from 'express';
import { fetchByRawWhere } from './lib/mysql-store';

const router = Router();

router.get('/catalog', async (req: Request, res: Response) => {
  const sku = req.query.sku as string;
  const rows = await fetchByRawWhere(`sku = '${sku}'`);
  res.json(rows);
});

export default router;
