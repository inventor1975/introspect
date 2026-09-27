const express = require('express');
const path = require('path');

const app = express();

app.get('/files/*', (req, res) => {
  const rel = req.params[0];
  const file = path.join(__dirname, 'public', rel);
  res.sendFile(file, { maxAge: '1h' }, (err) => {
    if (err) res.status(err.status || 404).end();
  });
});

app.listen(process.env.PORT || 3000);
