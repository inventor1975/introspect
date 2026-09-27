import express from 'express';
import { spawn } from 'node:child_process';

const app = express();

app.get('/media/probe', (req, res) => {
  const file = req.query.file;
  const child = spawn(`ffprobe -v quiet -print_format json -show_format ${file}`, {
    shell: true,
    cwd: '/srv/uploads',
  });
  let out = '';
  child.stdout.on('data', (chunk) => { out += chunk; });
  child.on('close', (code) => {
    if (code !== 0) return res.status(422).send('probe failed');
    res.type('json').send(out);
  });
});

export default app;
