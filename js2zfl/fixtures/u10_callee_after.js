const cp = require('child_process');
app.get('/', (req, res) => { cp.exec(outer(req.query.c)); });
function outer(v) { return inner(v); }
function inner(v) { return v; }   // REFUTED
