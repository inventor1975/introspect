import express from 'express';
import React from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { execFileSync } from 'child_process';

const MOUNTS: Record<string, string> = {
  home: '/home',
  data: '/srv/data',
  logs: '/var/log',
};

function QuotaPage({ volume, usage }: { volume: string; usage: string }) {
  return (
    <main>
      <h1>Usage for {volume}</h1>
      <pre>{usage}</pre>
    </main>
  );
}

const app = express();

app.get('/quota', (req, res) => {
  const volume = String(req.query.volume || 'home');
  if (!Object.prototype.hasOwnProperty.call(MOUNTS, volume)) {
    res.status(404).send('unknown volume');
    return;
  }
  const usage = execFileSync('df', ['-h', '--output=size,used,avail,pcent', MOUNTS[volume]], {
    encoding: 'utf8',
  });
  res.send('<!doctype html>' + renderToStaticMarkup(<QuotaPage volume={volume} usage={usage} />));
});

export default app;
