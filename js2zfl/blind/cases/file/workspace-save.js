const Koa = require('koa');
const Router = require('@koa/router');
const { koaBody } = require('koa-body');
const fs = require('fs');
const path = require('path');

const WORKSPACES = '/srv/workspaces';
const app = new Koa();
const router = new Router();

router.post('/workspaces/:owner/save', koaBody(), async (ctx) => {
  const { dir, filename, content } = ctx.request.body;
  if (!filename || typeof content !== 'string') {
    ctx.status = 422;
    ctx.body = { error: 'filename and content are required' };
    return;
  }
  const folder = path.join(WORKSPACES, ctx.params.owner, dir || '');
  fs.mkdirSync(folder, { recursive: true });
  fs.writeFileSync(path.join(folder, filename), content, 'utf8');
  ctx.body = { saved: true, bytes: Buffer.byteLength(content) };
});

app.use(router.routes());
module.exports = app;
