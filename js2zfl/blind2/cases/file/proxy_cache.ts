import express, { Request, Response } from 'express';
import { createHash } from 'crypto';
import { promises as fs } from 'fs';
import * as path from 'path';

const CACHE_DIR = path.join(__dirname, '..', '.image-cache');
const app = express();

function cacheKey(url: string): string {
  return createHash('sha256').update(url).digest('hex');
}

app.get('/img-proxy', async (req: Request, res: Response) => {
  const source = String(req.query.url || '');
  const cachedPath = path.join(CACHE_DIR, `${cacheKey(source)}.bin`);
  try {
    const cached = await fs.readFile(cachedPath);
    res.set('X-Cache', 'HIT').type('image/*').send(cached);
  } catch {
    res.status(404).json({ error: 'not cached yet', source });
  }
});

export default app;
