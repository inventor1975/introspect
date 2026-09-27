import { Router, Request, Response, NextFunction } from 'express';
import * as fs from 'fs';
import * as path from 'path';

const EXPORT_ROOT = path.resolve('/data/exports');

function cleanRelative(input: string): string {
  return input.replace(/\.\.\//g, '').replace(/^\/+/, '');
}

export const exportRouter = Router();

exportRouter.get('/exports/fetch', (req: Request, res: Response, next: NextFunction) => {
  const raw = String(req.query.path ?? '');
  const relative = cleanRelative(raw);
  const absolute = path.join(EXPORT_ROOT, relative);
  fs.readFile(absolute, (err, data) => {
    if (err) {
      return next(err);
    }
    res.type('application/octet-stream');
    res.send(data);
  });
});
