import { Router, Request, Response } from 'express';
import { alertBox } from './lib/views';

const router = Router();

router.get('/alert', (req: Request, res: Response) => {
  const text = (req.query.text as string) || 'Something happened.';
  res.send(alertBox(text, req.query.sticky !== '1'));
});

export default router;
