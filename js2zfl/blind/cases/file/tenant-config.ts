import express, { Request, Response } from 'express';
import { readFileSync } from 'node:fs';

const app = express();

function tenantOf(req: Request): string {
  return req.get('X-Tenant') || 'default';
}

app.get('/api/config', (req: Request, res: Response) => {
  const tenant = tenantOf(req);
  let cfg: Record<string, unknown>;
  try {
    cfg = JSON.parse(readFileSync(`/etc/app/tenants/${tenant}/config.json`, 'utf8'));
  } catch {
    res.status(404).json({ error: `unknown tenant` });
    return;
  }
  res.json({ tenant, features: cfg.features ?? [], branding: cfg.branding ?? null });
});

export default app;
