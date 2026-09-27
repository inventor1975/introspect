const express = require('express');
const { exec } = require('child_process');

const app = express();

function escapeHtml(s) {
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

app.get('/labels/print', (req, res) => {
  const printer = escapeHtml(req.query.printer);
  const copies = escapeHtml(req.query.copies || '1');
  exec(`lp -d ${printer} -n ${copies} /srv/labels/current.pdf`, (err, stdout) => {
    if (err) return res.status(500).send('<p>print failed</p>');
    res.send(`<p>Queued on ${printer}: ${escapeHtml(stdout)}</p>`);
  });
});

module.exports = app;
