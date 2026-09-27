import { Router, Request, Response } from 'express';
import { PrismaClient } from '@prisma/client';

const router = Router();
const prisma = new PrismaClient();

router.get('/audit', async (req: Request, res: Response) => {
  const actor = req.query.actor as string;
  const rows = await prisma.$queryRawUnsafe(
    `SELECT action, target, at FROM audit_log WHERE actor = '${actor}' ORDER BY at DESC`
  );
  res.json(rows);
});

export default router;
