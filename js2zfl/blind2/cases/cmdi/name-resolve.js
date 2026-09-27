const express = require('express');
const { execSync } = require('child_process');

const app = express();

app.get('/resolve', (req, res) => {
  const parts = ['nslookup'];
  if (req.query.server) {
    parts.push(req.query.host, req.query.server);
  } else {
    parts.push(req.query.host);
  }
  const text = execSync(parts.join(' '), { encoding: 'utf8', timeout: 5000 });
  res.send(`<pre>${text.replace(/</g, '&lt;')}</pre>`);
});

module.exports = app;
