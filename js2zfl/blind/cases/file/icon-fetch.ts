import { Router, Request, Response } from 'express';
import { readFileSync, existsSync } from 'fs';
import { join, basename, extname } from 'path';

const ICONS = join(__dirname, '..', 'assets', 'icons');
const ALLOWED_EXT = new Set(['.svg', '.png', '.ico']);

export const icons = Router();

icons.get('/icons', (req: Request, res: Response) => {
  const raw = String(req.query.name ?? '');
  const ext = extname(raw).toLowerCase();
  if (!ALLOWED_EXT.has(ext)) {
    return res.status(415).json({ error: `extension ${ext} not served` });
  }
  const file = join(ICONS, basename(raw));
  if (!existsSync(file)) {
    return res.sendStatus(404);
  }
  res.type(ext);
  return res.send(readFileSync(file));
});
