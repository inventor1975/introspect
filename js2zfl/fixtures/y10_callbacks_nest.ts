import { Controller, Get, Query } from '@nestjs/common';
import { validate as isUuid } from 'uuid';
import { exec } from 'child_process';
export function runIt(cmd) {
  return new Promise((resolve, reject) => { exec(cmd, (e, out) => resolve(out)); });   // a sink inside the executor
}
@Controller('w')
export class W {
  @Get() hello(@Query('name') name: string) { return '<h1>' + name + '</h1>'; }        // EXPECT: REFUTED (the body)
}
app.get('/r', async (req, res) => {
  await runIt('echo ' + req.query.x);                                                  // EXPECT: REFUTED (via the executor)
  const id = req.query.id;
  if (typeof id !== 'string' || !isUuid(id)) { return res.status(400).end(); }
  exec('rm /tmp/s/' + id);                                                             // clean: || of negated guards
});
