const cp = require('child_process');
const util = require('util');
const run = util.promisify(cp.exec);
app.get('/s', async (req, res) => {
  cp.spawn('sh', ['-c', 'tar czf out.tgz ' + req.query.dir]);          // EXPECT: REFUTED (a shell's script)
  cp.execFile('git', ['ls-remote', req.query.remote]);                 // EXPECT: OPEN (argument injection)
  await run('du -sh ' + req.query.p);                                  // EXPECT: REFUTED (promisify alias)
  require('child_process').exec('ping ' + req.query.h);                // EXPECT: REFUTED
  cp.spawn('sort', ['-r'], { input: req.body.rows });                  // clean: stdin is data for sort
  cp.exec('ls ' + req.query.d.replace(/[^a-z0-9_-]/g, ''));            // clean: a strip leaves no metacharacter
});
