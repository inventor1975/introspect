const express = require('express');
const { exec } = require('child_process');

const PRESETS = [
  'pandoc /srv/docs/handbook.md -o /srv/out/handbook.pdf',
  'pandoc /srv/docs/handbook.md -o /srv/out/handbook.epub',
  'pandoc /srv/docs/handbook.md -s -o /srv/out/handbook.html',
];

const app = express();

app.post('/docs/render', (req, res) => {
  const index = Number.parseInt(req.query.preset, 10);
  if (!(index >= 0 && index < PRESETS.length)) {
    return res.status(400).json({ error: 'unknown preset' });
  }
  exec(PRESETS[index], (err) => res.json({ preset: index, ok: !err }));
});

module.exports = app;
