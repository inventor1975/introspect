const Koa = require('koa');
const Router = require('@koa/router');
const fs = require('fs');
const path = require('path');

const INVOICES = path.join(__dirname, 'invoices');
const router = new Router();

router.get('/invoices/:id.pdf', async (ctx) => {
  const { id } = ctx.params;
  if (!/^\d{1,12}$/.test(id)) {
    ctx.throw(400, 'invalid invoice id');
  }
  const file = path.join(INVOICES, `INV-${id}.pdf`);
  if (!fs.existsSync(file)) ctx.throw(404);
  ctx.type = 'application/pdf';
  ctx.body = fs.createReadStream(file);
});

const app = new Koa();
app.use(router.routes()).use(router.allowedMethods());
module.exports = app;
