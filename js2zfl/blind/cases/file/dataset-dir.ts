import { Router } from 'express';
import type { Request, Response } from 'express';
import * as fs from 'node:fs';
import * as path from 'node:path';

const DATASETS = path.resolve(__dirname, '../datasets');
const router = Router();

router.get('/datasets/file', (req: Request, res: Response) => {
  const dir = String(req.query.dir ?? '');
  const fileName = path.basename(String(req.query.file ?? ''));
  const full = path.join(DATASETS, dir, fileName);
  fs.stat(full, (err, st) => {
    if (err || !st.isFile()) {
      res.sendStatus(404);
      return;
    }
    res.setHeader('Content-Length', st.size);
    fs.createReadStream(full).pipe(res);
  });
});

export default router;
