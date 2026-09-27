import express, { Request, Response, NextFunction } from 'express';
import { promises as fs } from 'node:fs';
import { Sandbox, OutsideSandboxError } from './lib/sandbox';

const sandbox = new Sandbox(process.env.WORKSPACE_ROOT ?? '/srv/workspace');
const app = express();
app.use(express.json());

app.put('/workspace/file', async (req: Request, res: Response, next: NextFunction) => {
  const { path: relPath, content } = req.body as { path: string; content: string };
  let target: string;
  try {
    target = sandbox.locate(relPath);
  } catch (err) {
    if (err instanceof OutsideSandboxError) {
      res.status(err.status).json({ error: 'path not allowed' });
      return;
    }
    next(err);
    return;
  }
  await fs.writeFile(target, content, 'utf8');
  res.status(204).end();
});

export default app;
