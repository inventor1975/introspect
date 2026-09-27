import express, { Request, Response, NextFunction } from 'express';
import path from 'path';

const REPORTS = path.join(__dirname, '..', 'generated-reports');
const router = express.Router();

router.get('/reports/export', (req: Request, res: Response, next: NextFunction) => {
  const file = req.query.file as string;
  if (!file) {
    res.status(400).send('file parameter missing');
    return;
  }
  res.download(file, `report-${Date.now()}.xlsx`, { root: REPORTS }, (err?: Error) => {
    if (err) next(err);
  });
});

export default router;
