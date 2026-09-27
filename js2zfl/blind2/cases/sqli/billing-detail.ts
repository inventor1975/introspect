import { Router, Request, Response } from 'express';
import { getRepository } from 'typeorm';
import { Charge } from './entities/charge';

const router = Router();

router.get('/charges/:id', async (req: Request, res: Response) => {
  const id = req.params.id;
  const repo = getRepository(Charge);
  const rows = await repo.query(
    'SELECT id, amount, status FROM charges WHERE id = $1',
    [id]
  );
  res.json(rows[0] || {});
});

export default router;
