const express = require('express');
const { exec } = require('child_process');

const app = express();
app.use(express.json());

const ACTIONS = new Map([
  ['restart-web', 'systemctl restart nginx'],
  ['flush-cache', 'redis-cli -n 2 FLUSHDB'],
  ['rotate-logs', 'logrotate -f /etc/logrotate.d/app'],
]);

app.post('/ops/run', (req, res) => {
  const action = req.body.action;
  const command = ACTIONS.get(action);
  if (!command) {
    return res.status(404).json({ error: 'unknown action', action });
  }
  exec(command, (err, stdout, stderr) => {
    res.json({ action, ok: !err, output: stdout || stderr });
  });
});

module.exports = app;
