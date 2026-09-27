const Koa = require('koa');
const Router = require('@koa/router');
const fs = require('fs');
const { PassThrough } = require('stream');

const router = new Router();

router.get('/ops/logs', async (ctx) => {
  const logName = ctx.query.log || 'app.log';
  const source = fs.createReadStream(`/var/log/myapp/${logName}`, { encoding: 'utf8' });
  const out = new PassThrough();
  source.on('error', (err) => out.destroy(err));
  source.pipe(out);
  ctx.type = 'text/plain';
  ctx.body = out;
});

const app = new Koa();
app.use(router.routes());
module.exports = app;
