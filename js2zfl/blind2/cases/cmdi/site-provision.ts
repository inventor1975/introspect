import express, { Request, Response } from 'express';
import { execSync } from 'child_process';

const app = express();
app.use(express.json());

function toSlug(input: string): string {
  return input.toLowerCase().replace(/[^a-z0-9_-]/g, '').slice(0, 40);
}

app.post('/sites', (req: Request, res: Response) => {
  const slug = toSlug(String(req.body.title || ''));
  if (!slug) {
    return res.status(400).json({ error: 'title produces empty slug' });
  }
  execSync(`mkdir -p /srv/sites/${slug}/public && cp -r /srv/skeleton/. /srv/sites/${slug}/`);
  res.status(201).json({ slug });
});

export default app;
