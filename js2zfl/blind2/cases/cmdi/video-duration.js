const express = require('express');
const childProcess = require('child_process');

const router = express.Router();

router.post('/videos/duration', express.json(), (req, res) => {
  const { filename } = req.body;
  const script = 'ffprobe -v error -show_entries format=duration -of csv=p=0 /srv/videos/' + filename;
  const proc = childProcess.spawn('sh', ['-c', script]);
  let buf = '';
  proc.stdout.on('data', (d) => (buf += d));
  proc.on('exit', () => res.json({ duration: parseFloat(buf) }));
});

module.exports = router;
