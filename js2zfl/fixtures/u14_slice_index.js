app.get('/u/:from', (req, res) => {
  const names = ['a', 'b'];
  res.send('users ' + names.slice(req.params.from).join(', '));   // EXPECT nothing: slice's argument is a number
});
