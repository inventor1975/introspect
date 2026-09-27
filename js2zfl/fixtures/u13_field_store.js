app.post('/pet', (req, res) => {
  req.pet.name = req.body.name;           // stores into ONE field
  res.redirect('/pet/' + req.pet.id);     // EXPECT OPEN (req may hold it), not REFUTED
});
