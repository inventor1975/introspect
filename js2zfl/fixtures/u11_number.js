const cp = require('child_process');
app.get('/', (req, res) => { const n = Number(req.query.n); cp.exec('sleep ' + n); });  // nothing
