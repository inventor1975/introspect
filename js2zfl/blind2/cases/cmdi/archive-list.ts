import { Router, Request, Response } from 'express';
import { exec } from 'child_process';
import { shellEscape } from './lib/shell';

export const archiveRouter = Router();

archiveRouter.get('/archives/:name/contents', (req: Request, res: Response) => {
  const archive = `/srv/archives/${req.params.name}`;
  const filter = String(req.query.filter || '');
  const cmd = `tar -tzf ${shellEscape(archive)} | grep -F -- ${shellEscape(filter)}`;
  exec(cmd, (err, stdout) => {
    if (err && !stdout) {
      res.json({ entries: [] });
      return;
    }
    res.json({ entries: stdout.split('\n').filter(Boolean) });
  });
});
