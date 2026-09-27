const cp = require('child_process');
app.get('/', (req, res) => { const o = {}; o.cmd = req.query.c; cp.exec(o.cmd); });  // REFUTED
