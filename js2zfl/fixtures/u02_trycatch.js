const cp = require('child_process');
app.get('/', (req, res) => { let c; try { c = req.query.c; } catch (e) { c = 'ls'; } cp.exec(c); });  // REFUTED
