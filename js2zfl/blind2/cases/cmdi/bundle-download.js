const express = require('express');
const { exec } = require('child_process');

const app = express();

app.get('/download/bundle', (req, res) => {
  const kind = req.query.kind;
  let cmd;
  switch (kind) {
    case 'zip':
      cmd = 'zip -qr - /srv/public';
      break;
    case 'tgz':
      cmd = 'tar -czf - /srv/public';
      break;
    case 'txz':
      cmd = 'tar -cJf - /srv/public';
      break;
    default:
      return res.status(400).send('unsupported format: ' + kind);
  }
  exec(cmd, { encoding: 'buffer', maxBuffer: 256 * 1024 * 1024 }, (err, stdout) => {
    if (err) return res.sendStatus(500);
    res.attachment(`public.${kind}`).send(stdout);
  });
});

module.exports = app;
