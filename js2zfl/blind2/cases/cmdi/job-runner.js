const express = require('express');
const { exec } = require('child_process');

const app = express();
app.use(express.json());

function buildJob(body) {
  const job = {
    cwd: '/srv/jobs',
    timeout: 60000,
    cmd: 'make',
  };
  if (body.target) {
    job.cmd = job.cmd + ' ' + body.target;
  }
  return job;
}

app.post('/build', (req, res) => {
  const job = buildJob(req.body);
  exec(job.cmd, { cwd: job.cwd, timeout: job.timeout }, (err, stdout, stderr) => {
    res.json({ ok: !err, stdout, stderr });
  });
});

module.exports = app;
