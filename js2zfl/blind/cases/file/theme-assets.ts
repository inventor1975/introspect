import { Router, Request, Response } from 'express';
import * as fs from 'node:fs';
import { resolveUnder, extensionOf, THEMES_ROOT } from './lib/paths';

const MIME: Record<string, string> = {
  '.css': 'text/css',
  '.svg': 'image/svg+xml',
  '.woff2': 'font/woff2',
};

export default function themeRoutes(router: Router): void {
  router.get('/themes/:theme/asset', (req: Request, res: Response) => {
    const theme = req.params.theme;
    const asset = String(req.query.path ?? 'style.css');
    const file = resolveUnder(`${THEMES_ROOT}/${theme}`, asset);
    let data: Buffer;
    try {
      data = fs.readFileSync(file);
    } catch {
      res.sendStatus(404);
      return;
    }
    res.type(MIME[extensionOf(file)] ?? 'application/octet-stream');
    res.end(data);
  });
}
