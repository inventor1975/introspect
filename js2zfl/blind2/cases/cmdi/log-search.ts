import { Router, Request, Response } from 'express';
import { exec } from 'child_process';

export const logsRouter = Router();

logsRouter.get('/logs/search', (req: Request, res: Response) => {
  let term = String(req.query.q || '');
  term = term.replace(';', '').replace('|', '').replace('&', '');
  exec(`grep -i ${term} /var/log/app/current.log | tail -n 200`, (err, stdout) => {
    if (err && !stdout) {
      return res.json({ matches: [] });
    }
    res.json({ matches: stdout.split('\n') });
  });
});
