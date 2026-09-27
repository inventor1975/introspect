const express = require('express');
const { exec } = require('child_process');

const app = express();
const HOST_RE = /^[a-z0-9.-]+$/i;

app.get('/certs/inspect', (req, res) => {
  const host = req.query.host;
  const port = req.query.port || '443';
  if (!HOST_RE.test(host)) {
    return res.status(400).send('invalid host');
  }
  exec(
    `echo | openssl s_client -servername ${host} -connect ${host}:${port} 2>/dev/null | openssl x509 -noout -dates`,
    (err, stdout) => res.type('text').send(err ? 'error' : stdout)
  );
});

module.exports = app;
