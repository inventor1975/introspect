const cp = require('child_process'); const lib = require('lib');
function h(s) { return lib.f(s); }
app.get('/', (req, res) => { cp.exec(h(req.query.c)); });   // EXPECT OPEN
