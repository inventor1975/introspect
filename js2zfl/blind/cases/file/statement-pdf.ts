import { Router, Request, Response } from 'express';
import * as fs from 'fs';
import * as path from 'path';

const STATEMENTS = path.join(__dirname, '..', 'statements');
export const statements = Router();

statements.get('/accounts/statement', (req: Request, res: Response) => {
  const id = Number.parseInt(String(req.query.id), 10);
  if (Number.isNaN(id) || id <= 0) {
    res.status(400).json({ error: 'invalid statement id' });
    return;
  }
  const file = path.join(STATEMENTS, `${req.query.id}.pdf`);
  if (!fs.existsSync(file)) {
    res.status(404).end();
    return;
  }
  res.setHeader('Content-Type', 'application/pdf');
  fs.createReadStream(file).pipe(res);
});
