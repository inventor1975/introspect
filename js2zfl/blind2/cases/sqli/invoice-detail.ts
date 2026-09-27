import { Router, Request, Response } from 'express';
import { getRepository } from 'typeorm';
import { Invoice } from './entities/invoice';

const router = Router();

router.get('/invoices/:number', async (req: Request, res: Response) => {
  const number = req.params.number;
  const repo = getRepository(Invoice);
  const rows = await repo.query(
    `SELECT * FROM invoices WHERE invoice_number = '${number}'`
  );
  res.json(rows);
});

export default router;
