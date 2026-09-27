const cp = require('child_process'); const escapeHtml = require('escape-html');
app.get('/', (req, res) => { const s = escapeHtml(req.query.c); res.send(s); cp.exec('echo ' + s); });  // REFUTED shell only
