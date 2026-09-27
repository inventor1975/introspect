const express = require('express');
const { exec } = require('child_process');

const app = express();
app.use(express.json());

function resolveEnvironment(req, res, next) {
  res.locals.environment = req.body.environment || req.query.env || 'staging';
  next();
}

app.post('/deploy', resolveEnvironment, (req, res) => {
  const env = res.locals.environment;
  exec(`./scripts/deploy.sh ${env}`, { cwd: '/srv/app' }, (err, stdout) => {
    if (err) return res.status(500).json({ error: 'deploy failed' });
    res.json({ env, log: stdout.split('\n').slice(-20) });
  });
});

module.exports = app;
