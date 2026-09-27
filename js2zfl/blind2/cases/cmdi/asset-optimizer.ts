import express, { Request, Response } from 'express';
import { execa } from 'execa';

const app = express();

app.get('/assets/optimize', async (req: Request, res: Response) => {
  const asset = String(req.query.asset);
  const quality = String(req.query.quality ?? '80');
  const { stdout } = await execa(`cwebp -q ${quality} /srv/assets/${asset} -o /srv/assets/${asset}.webp`, {
    shell: true,
  });
  res.json({ ok: true, stdout });
});

export default app;
