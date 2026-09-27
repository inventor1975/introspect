import { Router, Request, Response } from 'express';
import { PrismaClient, Prisma } from '@prisma/client';

const router = Router();
const prisma = new PrismaClient();

router.get('/access', async (req: Request, res: Response) => {
  const role = req.query.role as string;
  const rows = await prisma.$queryRaw(
    Prisma.sql`SELECT user_id, granted_at FROM access WHERE role = ${role}`
  );
  res.json(rows);
});

export default router;
