import { Router, Request, Response, NextFunction } from 'express';
import { promises as fs } from 'node:fs';
import path from 'node:path';

const PROJECTS_ROOT = path.resolve(process.env.PROJECTS_ROOT ?? '/srv/projects');
export const projectFiles = Router();

projectFiles.get('/projects/:project/raw', async (req: Request, res: Response, next: NextFunction) => {
  const projectRoot = path.join(PROJECTS_ROOT, 'workspace');
  const full = path.resolve(projectRoot, String(req.query.path ?? ''));
  const rel = path.relative(projectRoot, full);
  if (rel === '' || rel.startsWith('..') || path.isAbsolute(rel)) {
    res.status(400).json({ error: 'path outside project' });
    return;
  }
  try {
    const content = await fs.readFile(full);
    res.type('text/plain').send(content);
  } catch (e) {
    next(e);
  }
});
