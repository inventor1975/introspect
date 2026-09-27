import express, { Request, Response } from 'express';
import escapeHtml from 'escape-html';

const app = express();

app.get('/share', (req: Request, res: Response) => {
  const title = String(req.query.title || 'Check this out');
  const tweet = `https://twitter.com/intent/tweet?text=${encodeURIComponent(title)}`;
  const mail = `mailto:?subject=${encodeURIComponent(title)}`;
  res.send(`
    <p>Share &ldquo;${escapeHtml(title)}&rdquo;</p>
    <a href="${tweet}">Tweet</a>
    <a href="${mail}">Email</a>
  `);
});

export default app;
