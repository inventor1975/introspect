import Koa, { Context, Next } from 'koa';
import Router from '@koa/router';
import { createReadStream } from 'node:fs';
import path from 'node:path';

const FILES_ROOT = path.resolve('/srv/files/public');

async function resolveRequestedFile(ctx: Context, next: Next): Promise<void> {
  const requested = String(ctx.query.path ?? '');
  const full = path.resolve(FILES_ROOT, requested);
  if (!full.startsWith(FILES_ROOT + path.sep)) {
    ctx.throw(403, 'outside of public files');
  }
  ctx.state.filePath = full;
  await next();
}

const router = new Router();

router.get('/files', resolveRequestedFile, async (ctx: Context) => {
  const filePath: string = ctx.state.filePath;
  ctx.attachment(path.basename(filePath));
  ctx.body = createReadStream(filePath);
});

const app = new Koa();
app.use(router.routes());
export default app;
