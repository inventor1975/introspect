const cp = require('child_process');
function h(p, f) { if (f) { return p; } p = 'x'; return p; }
app.get('/', (req, res) => { cp.exec(h(req.query.c, true)); });  // REFUTED
