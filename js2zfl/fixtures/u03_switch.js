const cp = require('child_process');
app.get('/', (req, res) => { let c = 'ls'; switch (req.query.m) { case 'a': c = req.query.c; break; case 'b': c = 'pwd'; break; } cp.exec(c); }); // REFUTED
