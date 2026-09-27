import express, { Request, Response } from 'express';
import sanitizeHtml from 'sanitize-html';

const app = express();
app.use(express.json());

app.post('/forum/posts/preview', (req: Request, res: Response) => {
  const subject = sanitizeHtml(String(req.body.subject || ''), { allowedTags: [], allowedAttributes: {} });
  const body = sanitizeHtml(String(req.body.body || ''));
  res.send(`<article><h2>${subject}</h2><div class="post-body">${body}</div></article>`);
});

export default app;
