import express, { Request, Response } from 'express';

const app = express();

interface RemoteProfile {
  displayName: string;
  headline: string;
}

app.get('/people/:user', async (req: Request, res: Response) => {
  const url = `https://directory.example.org/api/profiles/${encodeURIComponent(req.params.user)}`;
  const upstream = await fetch(url);
  if (!upstream.ok) {
    res.status(502).send('<p>Directory unavailable.</p>');
    return;
  }
  const profile = (await upstream.json()) as RemoteProfile;
  res.send(`<h2>${profile.displayName}</h2><p>${profile.headline}</p>`);
});

export default app;
