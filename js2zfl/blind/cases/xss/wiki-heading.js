const Koa = require('koa');
const Router = require('@koa/router');

const app = new Koa();
const router = new Router();

router.get('/wiki/:slug', async (ctx) => {
  const slug = ctx.params.slug.replace(/-/g, ' ');
  ctx.body = '<h2>' + slug + '</h2><p>This page does not exist yet.</p>';
});

app.use(router.routes()).use(router.allowedMethods());

module.exports = app;
