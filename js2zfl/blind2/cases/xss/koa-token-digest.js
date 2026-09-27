const Koa = require('koa');
const Router = require('@koa/router');
const crypto = require('crypto');

const app = new Koa();
const router = new Router();

router.get('/tokens/fingerprint', async (ctx) => {
  const token = ctx.query.token || '';
  const digest = crypto.createHash('sha256').update(token).digest('hex');
  ctx.type = 'html';
  ctx.body = `<p>Fingerprint: <code>${digest.slice(0, 16)}</code></p>`;
});

app.use(router.routes());

module.exports = app;
