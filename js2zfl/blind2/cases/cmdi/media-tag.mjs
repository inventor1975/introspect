import express from 'express';
import { spawn } from 'node:child_process';
import { randomUUID } from 'node:crypto';

const app = express();
app.use(express.json());

app.post('/tracks/:id/retag', (req, res) => {
  const id = Number(req.params.id);
  if (!Number.isSafeInteger(id)) return res.status(400).end();
  const { title = '', artist = '' } = req.body;
  const input = `/srv/tracks/${id}.mp3`;
  const output = `/srv/tracks/tmp-${randomUUID()}.mp3`;
  const ff = spawn('ffmpeg', [
    '-y', '-i', input,
    '-metadata', `title=${title}`,
    '-metadata', `artist=${artist}`,
    '-codec', 'copy', output,
  ], { shell: false });
  ff.on('close', (code) => res.status(code === 0 ? 200 : 500).json({ output }));
});

export default app;
