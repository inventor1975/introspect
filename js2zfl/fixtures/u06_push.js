const cp = require('child_process');
app.get('/', (req, res) => { const a = ['ls']; a.push(req.query.c); cp.exec(a.join(' ')); });  // REFUTED
