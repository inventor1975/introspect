const Koa = require('koa');
const Router = require('@koa/router');
const fs = require('fs');
const path = require('path');

const DOCS = path.join(__dirname, 'content', 'docs');
const app = new Koa();
const router = new Router({ prefix: '/docs' });

router.get('/:page', async (ctx) => {
  const page = ctx.params.page;
  const file = `${DOCS}/${page}.md`;
  try {
    await fs.promises.access(file, fs.constants.R_OK);
  } catch (e) {
    ctx.throw(404, 'no such page');
  }
  ctx.type = 'text/markdown; charset=utf-8';
  ctx.body = fs.createReadStream(file);
});

app.use(router.routes()).use(router.allowedMethods());

module.exports = app;
