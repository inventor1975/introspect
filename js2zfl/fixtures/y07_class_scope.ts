export class C {
  show = (req, res) => { res.send('<p>' + req.query.q + '</p>'); };   // EXPECT: REFUTED (a class-property handler)
}
export const s = (req, res) => {
  const title = 'Home';
  if (req.query.from) { const title = req.query.from; console.log(title); }
  res.send('<h1>' + title + '</h1>');                                // clean: the inner const is block-scoped
};
