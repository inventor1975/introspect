import { Router, Request, Response } from 'express';
import { noticeBox } from './lib/views';

const router = Router();

router.get('/notice', (req: Request, res: Response) => {
  const text = (req.query.text as string) || 'Nothing to report.';
  const level = req.query.level === 'warn' ? 'warn' : 'info';
  res.send(noticeBox(text, level));
});

export default router;
