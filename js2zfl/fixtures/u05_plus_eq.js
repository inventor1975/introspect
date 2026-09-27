const cp = require('child_process');
app.get('/', (req, res) => { let c = req.query.c; c += ' -la'; cp.exec(c); });  // REFUTED (was: += read as =)
