import express, { Request, Response } from 'express';
import sanitizeHtml from 'sanitize-html';

const app = express();
app.use(express.json());

const SIGNATURE_OPTIONS: sanitizeHtml.IOptions = {
  allowedTags: ['a', 'b', 'i', 'em', 'strong', 'span'],
  allowedAttributes: false,
};

app.post('/forum/signature', (req: Request, res: Response) => {
  const signature = sanitizeHtml(String(req.body.signature || ''), SIGNATURE_OPTIONS);
  res.send(`<div class="signature">${signature}</div>`);
});

export default app;
