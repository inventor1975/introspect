const express = require('express');

const app = express();

app.get('/welcome', ({ query: { name = 'guest' } }, res) =>
  res.status(200).send('<div class="welcome">Welcome back, ' + name + '!</div>')
);

app.listen(3000);
