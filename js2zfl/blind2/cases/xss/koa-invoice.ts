import Koa from 'koa';
import Router from '@koa/router';

const app = new Koa();
const router = new Router();

router.get('/invoices/:id', async (ctx) => {
  const id = Number(ctx.params.id);
  if (!Number.isInteger(id) || id <= 0) {
    ctx.status = 400;
    ctx.body = '<p>Invalid invoice number.</p>';
    return;
  }
  ctx.type = 'html';
  ctx.body = `<h1>Invoice #${id}</h1><a href="/invoices/${id}/pdf">Download PDF</a>`;
});

app.use(router.routes());

export default app;
