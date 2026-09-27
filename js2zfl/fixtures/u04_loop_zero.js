const cp = require('child_process');
app.get('/', (req, res) => { let c = req.query.c; for (const x of []) { c = 'ls'; } cp.exec(c); });  // REFUTED
