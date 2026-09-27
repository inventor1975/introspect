const express = require('express');

const app = express();
const auditLog = [];

app.get('/account/export', (req, res) => {
  const reason = req.query.reason;
  console.log(`[audit] export requested from ${req.ip} reason=${reason}`);
  auditLog.push({ at: Date.now(), reason });
  res.send('<p>Your export has been queued. We will email you when it is ready.</p>');
});

module.exports = app;
