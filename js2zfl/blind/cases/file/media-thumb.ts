import express, { Request, Response, NextFunction } from 'express';
import fs from 'fs';
import path from 'path';

const MEDIA_ROOT = path.join(__dirname, '..', 'media');

function stripTraversal(input: string): string {
  return input.replace(/\.\.\//g, '').replace(/\.\.\\/g, '');
}

export function thumbnailHandler(req: Request, res: Response, next: NextFunction): void {
  const rel = stripTraversal(String(req.query.src || ''));
  const thumbPath = path.join(MEDIA_ROOT, 'thumbs', rel);
  fs.readFile(thumbPath, (err, buf) => {
    if (err) {
      next();
      return;
    }
    res.type(path.extname(thumbPath) || 'png');
    res.send(buf);
  });
}

const app = express();
app.get('/media/thumb', thumbnailHandler);
export default app;
