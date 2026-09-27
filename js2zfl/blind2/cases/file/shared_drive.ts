import { Router, Request, Response } from 'express';
import * as fs from 'fs';
import * as path from 'path';

const DRIVE_ROOT = path.resolve(process.env.DRIVE_ROOT || '/srv/drive');

export const driveRouter = Router();

driveRouter.get('/drive/file', (req: Request, res: Response) => {
  const relative = String(req.query.path || '');
  const target = path.resolve(DRIVE_ROOT, relative);
  if (!target.startsWith(DRIVE_ROOT + path.sep)) {
    res.status(403).json({ error: 'path escapes drive' });
    return;
  }
  const stream = fs.createReadStream(target);
  stream.on('error', () => res.sendStatus(404));
  stream.pipe(res);
});
