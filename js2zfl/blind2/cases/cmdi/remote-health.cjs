'use strict';

const express = require('express');

const app = express();
app.use(express.json());

app.post('/fleet/health', (req, res) => {
  const { host, user } = req.body;
  const login = (user || 'monitor') + '@' + host;
  require('child_process').exec(
    'ssh -o BatchMode=yes -o ConnectTimeout=5 ' + login + ' uptime',
    (err, stdout) => {
      res.json({ host, reachable: !err, uptime: stdout && stdout.trim() });
    }
  );
});

module.exports = app;
