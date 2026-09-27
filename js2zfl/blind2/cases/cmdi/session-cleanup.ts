import express, { Request, Response } from 'express';
import { exec } from 'child_process';
import { validate as isUuid } from 'uuid';

const app = express();

app.delete('/sessions/:sessionId/scratch', (req: Request, res: Response) => {
  const { sessionId } = req.params;
  if (!isUuid(sessionId)) {
    return res.status(400).json({ error: 'invalid session id' });
  }
  exec(`rm -rf /srv/scratch/${sessionId}`, (err) => {
    res.status(err ? 500 : 204).end();
  });
});

export default app;
