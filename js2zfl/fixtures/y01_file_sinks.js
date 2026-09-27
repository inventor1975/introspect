const express = require('express');
const { readFile } = require('fs/promises');
const send = require('koa-send');
const app = express();
app.get('/a', async (req, res) => {
  await readFile('/srv/' + req.query.f);                 // EXPECT: REFUTED (imported by name)
  res.sendFile('/srv/' + req.query.f);                   // EXPECT: REFUTED (a path)
  res.sendFile(req.query.f, { root: '/srv/public' });    // clean: root confines it
});
async function k(ctx) { await send(ctx, ctx.query.file, { root: '/' }); }   // EXPECT: REFUTED (root '/')
