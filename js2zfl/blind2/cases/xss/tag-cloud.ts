import { Router, Request, Response } from 'express';

export const tags = Router();

tags.get('/tags', (req: Request, res: Response) => {
  const raw = String(req.query.tags ?? '');
  const parts = raw
    .split(',')
    .map((t) => t.trim())
    .filter(Boolean);

  let html = '<ul class="tags">';
  for (const tag of parts) {
    html += '<li>' + tag + '</li>';
  }
  html += '</ul>';

  res.type('html').send(html);
});
