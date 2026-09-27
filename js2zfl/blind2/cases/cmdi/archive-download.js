const express = require('express');
const { exec } = require('child_process');

const app = express();

app.get('/download/archive', (req, res) => {
  const kind = req.query.kind;
  let cmd;
  switch (kind) {
    case 'zip':
      cmd = 'zip -r - /srv/public';
      break;
    case 'tgz':
      cmd = 'tar -czf - /srv/public';
      break;
    default:
      cmd = `${kind} /srv/public`;
  }
  exec(cmd, { encoding: 'buffer', maxBuffer: 256 * 1024 * 1024 }, (err, stdout) => {
    if (err) return res.sendStatus(500);
    res.attachment(`public.${kind}`).send(stdout);
  });
});

module.exports = app;
