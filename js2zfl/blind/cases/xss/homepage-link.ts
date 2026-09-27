import express, { Request, Response } from 'express';
import escapeHtml from 'escape-html';

const app = express();

function httpUrlOrNull(candidate: string): string | null {
  try {
    const url = new URL(candidate);
    return url.protocol === 'http:' || url.protocol === 'https:' ? url.href : null;
  } catch {
    return null;
  }
}

app.get('/members/:handle', (req: Request, res: Response) => {
  const handle = escapeHtml(req.params.handle);
  const site = httpUrlOrNull(String(req.query.website || ''));
  const link = site ? `<a rel="nofollow" href="${escapeHtml(site)}">Website</a>` : '';
  res.send(`<div class="member"><h2>@${handle}</h2>${link}</div>`);
});

export default app;
