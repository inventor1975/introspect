import { Router, Request, Response } from 'express';
import { PrismaClient } from '@prisma/client';

const router = Router();
const prisma = new PrismaClient();

router.get('/subscriptions', async (req: Request, res: Response) => {
  const plan = req.query.plan as string;
  const rows = await prisma.subscription.findMany({
    where: { plan },
    take: 50,
    orderBy: { createdAt: 'desc' },
  });
  res.json(rows);
});

export default router;
