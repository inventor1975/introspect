import express, { Request, Response } from 'express';

const app = express();

app.get('/catalog', (req: Request, res: Response) => {
  const page = parseInt(String(req.query.page ?? '1'), 10);
  const size = Math.min(parseInt(String(req.query.size ?? '20'), 10) || 20, 100);
  res.send(`<nav class="pager"><span>Page ${page}</span> <span>(${size} per page)</span></nav>`);
});

export default app;
