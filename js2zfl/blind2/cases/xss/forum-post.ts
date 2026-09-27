import express, { Request, Response } from 'express';
import sanitizeHtml from 'sanitize-html';

const app = express();
app.use(express.json());

const POLICY: sanitizeHtml.IOptions = {
  allowedTags: ['b', 'i', 'em', 'strong', 'p', 'br', 'ul', 'ol', 'li'],
  allowedAttributes: {},
};

app.post('/forum/posts/render', (req: Request, res: Response) => {
  const body = sanitizeHtml(String(req.body.body ?? ''), POLICY);
  res.send(`<div class="post-body">${body}</div>`);
});

export default app;
