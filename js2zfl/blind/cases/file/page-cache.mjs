import express from 'express';
import { createHash } from 'node:crypto';
import { readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';

const CACHE_DIR = path.resolve('var/cache/pages');
const app = express();

function cacheFileFor(url) {
  const digest = createHash('sha256').update(url).digest('hex');
  return path.join(CACHE_DIR, `${digest}.html`);
}

app.get('/render', async (req, res) => {
  const target = String(req.query.url || '/');
  const cacheFile = cacheFileFor(target);
  try {
    const cached = await readFile(cacheFile, 'utf8');
    return res.type('html').send(cached);
  } catch {
    // cache miss
  }
  const html = `<!doctype html><p>rendered at ${new Date().toISOString()}</p>`;
  await writeFile(cacheFile, html);
  res.type('html').send(html);
});

export default app;
