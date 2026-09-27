import { Router, Request, Response } from 'express';
import { exec } from 'child_process';

const router = Router();

router.get('/net/port-owner', (req: Request, res: Response) => {
  const port = Number(req.query.port);
  if (!Number.isInteger(port) || port < 1 || port > 65535) {
    res.status(400).json({ error: `invalid port ${req.query.port}` });
    return;
  }
  exec(`lsof -nP -iTCP:${port} -sTCP:LISTEN`, (err, stdout) => {
    res.json({ port, listening: !err, detail: stdout });
  });
});

export default router;
