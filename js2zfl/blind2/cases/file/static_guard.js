const Koa = require('koa');
const Router = require('@koa/router');
const fs = require('fs');
const path = require('path');

const STATIC_ROOT = path.resolve(__dirname, 'public');
const router = new Router();

function insideRoot(root, candidate) {
  const rel = path.relative(root, candidate);
  return rel !== '' && !rel.startsWith('..') && !path.isAbsolute(rel);
}

router.get('/static/:file(.*)', async (ctx) => {
  const candidate = path.join(STATIC_ROOT, ctx.params.file);
  if (!insideRoot(STATIC_ROOT, candidate)) {
    ctx.throw(403, 'forbidden');
  }
  ctx.type = path.extname(candidate);
  ctx.body = fs.createReadStream(candidate);
});

const app = new Koa();
app.use(router.routes());
module.exports = app;
