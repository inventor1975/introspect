async function a(ctx) { ctx.body = `<h1>${ctx.query.q}</h1>`; }                 // EXPECT: REFUTED
async function b(ctx) { ctx.type = 'text/plain'; ctx.set('X-Content-Type-Options', 'nosniff'); ctx.body = ctx.query.q; }  // clean
async function c(ctx) { ctx.body = { q: ctx.query.q }; }                         // clean: JSON
