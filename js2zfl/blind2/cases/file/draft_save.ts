import Koa from 'koa';
import Router from '@koa/router';
import bodyParser from 'koa-bodyparser';
import { promises as fs } from 'fs';
import * as path from 'path';

const DRAFTS = path.join(__dirname, '..', 'drafts');

type DraftBody = { path: string; content: string };

const router = new Router({ prefix: '/drafts' });

router.post('/', async (ctx: Koa.Context) => {
  const body = ctx.request.body as DraftBody;
  if (typeof body.content !== 'string') {
    ctx.throw(400, 'content missing');
  }
  const destination = path.join(DRAFTS, body.path);
  await fs.mkdir(path.dirname(destination), { recursive: true });
  await fs.writeFile(destination, body.content, 'utf8');
  ctx.status = 201;
  ctx.body = { saved: body.path };
});

const app = new Koa();
app.use(bodyParser());
app.use(router.routes());

export default app;
