import Koa, { Context } from 'koa';
import Router from '@koa/router';
import { promises as fs } from 'fs';
import path from 'path';

const router = new Router();

async function loadTemplate(name: string): Promise<string> {
  const file = path.resolve('views/mail', name);
  return fs.readFile(file, 'utf8');
}

router.get('/mail/templates', async (ctx: Context) => {
  const template = (ctx.query.template as string) || 'reset-password.hbs';
  try {
    ctx.body = { template, source: await loadTemplate(template) };
  } catch {
    ctx.status = 404;
    ctx.body = { error: 'template not found' };
  }
});

const app = new Koa();
app.use(router.routes());
export default app;
